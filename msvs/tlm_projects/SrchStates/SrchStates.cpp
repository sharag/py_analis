// SrchStates.cpp: ���������� ����� ����� ��� ����������� ����������.
//

#include "stdafx.h"

typedef unsigned int uint;
typedef unsigned char uchar;
typedef unsigned short ushort;

/*��������� �������*/
char inFILEpath[FILENAME_MAX * sizeof(char)];//���� � �������� � ASKI
											 /*��������� ��������*/
float fdiskr;//������� ������������� ������ � ��
float timeIntrvl; //����������� �������� ������� ������ � ����� ������
uint numorder;//���������� �������� ������
uint minNumMode;//����������� ���������� ������������������ �������
uint maxNumMode;//������������ ���������� ������������������ �������
				/*�������������� �������������� �����*/
uint numword;
uint fsize;//������ �����
uint numModes = 0;//���������� ��������� ������� �������
uchar * data = NULL;//��������� �� ������ ������ �������� �����
UINT64 * wordsChan = NULL;//��������� �� ������ ���� ������*/

						  /*������� - �������*/
void Usage(char *programName)
{
	fprintf(stderr, "%s usage:\n", programName);
	fprintf(stderr, "%s -i <input files path, str> -o <number of order, uint[8, 16, 32, 64]> \
-t <time interval in one mode, float[0.1 - 300.0]> -f <sampling frequency in Hz, float> \
-l <minimum number of modes, uint[1 - 50]> -b <maximum number of modes, uint[1 - 50]>\n", programName);
}

/* returns the index of the first argument that is not an option; i.e.
does not start with a dash or a slash
���������� ���������� �����*/
int HandleOptions(int argc, char *argv[])
{
	int i, firstnonoption = 0;
	for (i = 1; i< argc; i++) {
		if (argv[i][0] == '/' || argv[i][0] == '-') {
			switch (argv[i][1]) {
			case '?':
			case 'h':
			case 'H':
				Usage(argv[0]);
				break;
			case 'i':
				sscanf_s(argv[i + 1], "%[^\r\n]s", inFILEpath, FILENAME_MAX);
				i++;
				break;
			case 'o':
				sscanf_s(argv[i + 1], "%d", &numorder);
				i++;
				break;
			case 't':
				sscanf_s(argv[i + 1], "%f", &timeIntrvl);
				i++;
				break;
			case 'f':
				sscanf_s(argv[i + 1], "%f", &fdiskr);
				i++;
				break;
			case 'l':
				sscanf_s(argv[i + 1], "%d", &minNumMode);
				i++;
				break;
			case 'b':
				sscanf_s(argv[i + 1], "%d", &maxNumMode);
				i++;
				break;
			default:
				fprintf(stderr, "LOG | WARNING | SrchStates | Unknown option %s\n", argv[i]);
				fprintf(stdout, "LOG | WARNING | SrchStates | Unknown option %s\n", argv[i]);
				Usage(argv[0]);
				break;
			}
		}
		else {
			firstnonoption = i;
			break;
		}
	}
	return firstnonoption;
}

/*������� ������ ������������� �������� �
������� ������������� �������� � �������*/
void getMax(uint * arrayVal, uint lenArray, uint * maxval, int * index)
{
	*maxval = 0;
	for (uint i = 1; i < lenArray; i++)
	{
		if (arrayVal[i] >(*maxval))
		{
			*maxval = arrayVal[i];
			*index = i;
		}
	}
}

/*��������� ������ �� 3 �������*/
UINT64 medFilt3(UINT64 a, UINT64 b, UINT64 c)
{
	UINT64 middle;
	if ((a <= b) && (a <= c))
		middle = (b <= c) ? b : c;
	else
		if ((b <= a) && (b <= c))
			middle = (a <= c) ? a : c;
		else
			middle = (a <= b) ? a : b;
	return middle;
}

/*������� ��� ������ ������ �� �����. ��������� ������ ��� ������ ��������
������������ �����.
������� ������: ��������� �� ����
���������� ����������: fsize
���������� 0 � ������ ���� � ��������� �� ������ � ������ ������*/
uchar * dataread(char * path)
{
	FILE *fileID;//��������� �� ������� ����
				 //�������� �����
	if (fopen_s(&fileID, path, "rb"))
	{
		fprintf(stdout, "LOG | WARNING | SrchStates | Error open file.\n");
		fprintf(stderr, "LOG | WARNING | SrchStates | Error open file.\n");
		return(0);
	}
	//����������� ������� �����
	fseek(fileID, 0, SEEK_END);
	fsize = ftell(fileID);
	fseek(fileID, 0, SEEK_SET);
	if (fsize == 0)
	{
		fprintf(stdout, "LOG | WARNING | SrchStates | File is 0 bytes.\n");
		fprintf(stderr, "LOG | WARNING | SrchStates | File is 0 bytes.\n");
		return(0);
	}
	else if (fsize > 10485760) //���� ������ ����� > 10 ��
	{
		fprintf(stdout, "LOG | WARNING | SrchStates | File is too large (> 10 Mb).\n");
		fprintf(stderr, "LOG | WARNING | SrchStates | File is too large (> 10 Mb).\n");
	}
	//��������� ������ ��� ������ ��������
	data = (uchar*)malloc(fsize);
	if (data == NULL)
	{
		fprintf(stdout, "LOG | CRITICAL | SrchStates | Memory allocation error.\n");
		fprintf(stderr, "LOG | CRITICAL | SrchStates | Memory allocation error.\n");
		return(0);
	}
	/*������ �����*/
	size_t result = fread(data, 1, fsize, fileID);
	if (result != fsize)
	{
		free(data);
		fprintf(stdout, "LOG | WARNING | SrchStates | Read error.\n");
		fprintf(stderr, "LOG | WARNING | SrchStates | Read error.\n");
		return(0);
	}

	fclose(fileID);
	fprintf(stdout, "LOG | INFO | SrchStates | Reading file complete.\n");
	return(data);
}

/*������� ������������� ��� ������������ ������� �������� ������
�� ������� ���� �� �����.
������� ������: ��������� �� ������ ���� ������
���������� ��������� �� ������ ���� ������
���������� ����������: ���������� �������� ����� ������*/
UINT64 * getValues(uchar * inArray)
{
	UINT64 * wordsChan_ = (UINT64*)malloc(numword * sizeof(UINT64));
	if (wordsChan_ == NULL)
	{
		fprintf(stdout, "LOG | CRITICAL | SrchStates | Memory allocation error.\n");
		fprintf(stderr, "LOG | CRITICAL | SrchStates | Memory allocation error.\n");
		return(0);
	}
	memset(wordsChan_, 0, numword * sizeof(UINT64));
	if (numorder == 8)
	{
		for (uint i = 0; i < numword; i++)
			wordsChan_[i] = ((UINT8*)inArray)[i];
	}
	else if (numorder == 16)
	{
		for (uint i = 0; i < numword; i++)
			wordsChan_[i] = ((UINT16*)inArray)[i];
	}
	else if (numorder == 32)
	{
		for (uint i = 0; i < numword; i++)
			wordsChan_[i] = ((UINT32*)inArray)[i];
	}
	else if (numorder == 64)
	{
		for (uint i = 0; i < numword; i++)
			wordsChan_[i] = ((UINT64*)inArray)[i];
	}
	return(wordsChan_);
}

bool findMode(UINT64 value, UINT64 * inList, uint lenList)
{
	for (uint i = 0; i < lenList; i++)
	{
		if (inList[i] == value)
			return(true);
		else if (inList[i] == 0)
			return(false);
	}
	return(false);
}

/*������� ������ ����, �������� ����������� ����������, ����������� ������
� �����, ���� ����������, ������������� ������������ ���������� ���,
���������� ��������� ���� ����������, ������������� ���� ���������
� ���������� ��������� (�������� �� ���� ���������).*/
bool srch_states(char * path)
{
	uint count = 0;//������� ������������ ��������
	UINT64 * modeList = NULL;// ������ ��������� �������. � ������� ����� �������� �������
	uint lenList = maxNumMode * 2 * sizeof(UINT64);
	numModes = 0;//���������� ��������� ������� �������
				 //������������� ������ ��������� �������
	modeList = (UINT64*)malloc(lenList);
	memset(modeList, 0, lenList);
	//������ �����
	data = dataread(path);
	//����������� ���������� ���� � ������
	numword = (uint)floor(fsize * 8 / (numorder));
	// ������������ ������� ��������
	// ��������� ��������� �� ������ ���� ������
	wordsChan = getValues(data);
	free(data);
	// ����� ������� �������
	for (uint i = 1; i < (numword - 2); i++)
	{
		// ��������� ����������
		wordsChan[i] = medFilt3(wordsChan[i], wordsChan[i + 1], wordsChan[i + 2]);

		if (wordsChan[i] == wordsChan[i - 1])
			count++;
		else
		{
			if ((count / fdiskr) >= timeIntrvl)
			{
				if (!findMode(wordsChan[i - 1], modeList, lenList))
				{
					modeList[numModes] = wordsChan[i - 1];
					numModes++;
				}
			}
			count = 0;
		}
		if (numModes > maxNumMode)
			break;
	}
	free(wordsChan);
	//����������� ���������� ��������� �������
	if (numModes > minNumMode && numModes < maxNumMode)
		return(true);
	else
		return(false);
}

/*�������� ������� ����������*/
int verification(char *argv[])
{
	if (strnlen_s(inFILEpath, FILENAME_MAX) < 3)
	{
		fprintf(stdout, "LOG | WARNING | SrchStates | Invalid input directory path.\n");
		fprintf(stderr, "LOG | WARNING | SrchStates | Invalid input directory path.\n");
	}
	else if (timeIntrvl > (float)300 || timeIntrvl < (float)0.1)
	{
		fprintf(stdout, "LOG | WARNING | SrchStates | Invalid time interval: float[0.1 - 300.0].\n");
		fprintf(stderr, "LOG | WARNING | SrchStates | Invalid time interval: float[0.1 - 300.0].\n");
	}
	else if (minNumMode < 1 || minNumMode > 50)
	{
		fprintf(stdout, "LOG | WARNING | SrchStates | Invalid minimum number of modes: uint[1 - 50].\n");
		fprintf(stderr, "LOG | WARNING | SrchStates | Invalid minimum number of modes: uint[1 - 50].\n");
	}
	else if (maxNumMode < 1 || maxNumMode > 50)
	{
		fprintf(stdout, "LOG | WARNING | SrchStates | Invalid maximum number of modes: uint[1 - 50].\n");
		fprintf(stderr, "LOG | WARNING | SrchStates | Invalid maximum number of modes: uint[1 - 50].\n");
	}
	else if (minNumMode >= maxNumMode)
	{
		fprintf(stdout, "LOG | WARNING | SrchStates | Minimum number of modes should be less than maximum number of modes.\n");
		fprintf(stderr, "LOG | WARNING | SrchStates | Minimum number of modes should be less than maximum number of modes.\n");
	}
	else
	{
		if (numorder != 8 && numorder != 16 && numorder != 32 && numorder != 64)
		{
			fprintf(stdout, "LOG | WARNING | SrchStates | Invalid number of order: uint[8, 16, 32, 64].\n");
			fprintf(stderr, "LOG | WARNING | SrchStates | Invalid number of order: uint[8, 16, 32, 64].\n");
			Usage(argv[0]);
			return (-1);
		}
		return(0);
	}
	Usage(argv[0]);
	return (-1);
}

int main(int argc, char *argv[])
{
	fdiskr = 100;//������� ������������� ������ � ��
	timeIntrvl = 1.0;//����������� ������� ������ � ����� ������
	numorder = 16;//���������� �������� ������
	minNumMode = 3;//����������� ���������� ������������������ �������
	maxNumMode = 17;//������������ ���������� ������������������ �������
	numword = 0;//���������� ��������
	fsize = 0;//������ �����
	memset(inFILEpath, 0, FILENAME_MAX * sizeof(wchar_t));

	/* handle the program options */
	HandleOptions(argc, argv);

	if (verification(argv))
		return (-1);
	
	if (srch_states(inFILEpath))
		fprintf(stdout, "LOG | INFO | SrchStates | TEST_STATUS | TRUE | FNAME | %s\n", inFILEpath);
	else
		fprintf(stdout, "LOG | INFO | SrchStates | TEST_STATUS | FALSE\n");
	return 0;
}

