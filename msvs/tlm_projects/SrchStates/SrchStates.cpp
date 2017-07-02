// SrchStates.cpp: определяет точку входа для консольного приложения.
//

#include "stdafx.h"

typedef unsigned int uint;
typedef unsigned char uchar;
typedef unsigned short ushort;

/*параметры запуска*/
char inFILEpath[FILENAME_MAX * sizeof(char)];//путь к каталогу в ASKI
											 /*параметры решателя*/
float fdiskr;//Частота дискретизации канала в Гц
float timeIntrvl; //Оцениваемый интервал времени работы в одном режиме
uint numorder;//Количество разрядов канала
uint minNumMode;//Минимальное количество идентифицированных режимов
uint maxNumMode;//Максимальное количество идентифицированных режимов
				/*рассчитываемые характеристики файла*/
uint numword;
uint fsize;//размер файла
uint numModes = 0;//Количество найденных каналов режимов
uchar * data = NULL;//указатель на массив данных входного файла
UINT64 * wordsChan = NULL;//Указатель на массив слов канала*/

						  /*Функция - справка*/
void Usage(char *programName)
{
	fprintf(stderr, "%s usage:\n", programName);
	fprintf(stderr, "%s -i <input files path, str> -o <number of order, uint[8, 16, 32, 64]> \
-t <time interval in one mode, float[0.1 - 300.0]> -f <sampling frequency in Hz, float> \
-l <minimum number of modes, uint[1 - 50]> -b <maximum number of modes, uint[1 - 50]>\n", programName);
}

/* returns the index of the first argument that is not an option; i.e.
does not start with a dash or a slash
Возвращает количество опций*/
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

/*Функция поиска максимального значения и
индекса максимального значения в массиве*/
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

/*Медианный фильтр на 3 отсчета*/
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

/*Функция для чтения данных из файла. Выделение памяти под массив значений
производится здесь.
Входные данные: указатель на путь
Глобальные переменные: fsize
Возвращает 0 в случае сбоя и указатель на массив в случае успеха*/
uchar * dataread(char * path)
{
	FILE *fileID;//указатель на входной файл
				 //открытие файла
	if (fopen_s(&fileID, path, "rb"))
	{
		fprintf(stdout, "LOG | WARNING | SrchStates | Error open file.\n");
		fprintf(stderr, "LOG | WARNING | SrchStates | Error open file.\n");
		return(0);
	}
	//определение размера файла
	fseek(fileID, 0, SEEK_END);
	fsize = ftell(fileID);
	fseek(fileID, 0, SEEK_SET);
	if (fsize == 0)
	{
		fprintf(stdout, "LOG | WARNING | SrchStates | File is 0 bytes.\n");
		fprintf(stderr, "LOG | WARNING | SrchStates | File is 0 bytes.\n");
		return(0);
	}
	else if (fsize > 10485760) //Если размер файла > 10 Мб
	{
		fprintf(stdout, "LOG | WARNING | SrchStates | File is too large (> 10 Mb).\n");
		fprintf(stderr, "LOG | WARNING | SrchStates | File is too large (> 10 Mb).\n");
	}
	//выделение памяти под массив значений
	data = (uchar*)malloc(fsize);
	if (data == NULL)
	{
		fprintf(stdout, "LOG | CRITICAL | SrchStates | Memory allocation error.\n");
		fprintf(stderr, "LOG | CRITICAL | SrchStates | Memory allocation error.\n");
		return(0);
	}
	/*чтение файла*/
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

/*Функция предназначена для формирования массива значений канала
из массива байт из файла.
Входные данные: указатель на массив слов данных
Возвращает указатель на массив слов канала
Глобальные переменные: количество разрядов слова канала*/
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

/*Функция читает файл, получает гистограммы приращений, преобразует данные
в слова, ищет приращения, встретившиеся максимальное количество раз,
сравнивает отношение двух приращений, встретившихся чаще остальных
и возвращает результат (является ли файл счетчиком).*/
bool srch_states(char * path)
{
	uint count = 0;//Счетчик неизменяемых значений
	UINT64 * modeList = NULL;// Список найденных каналов. В ячейках лежат значения каналов
	uint lenList = maxNumMode * 2 * sizeof(UINT64);
	numModes = 0;//Количество найденных каналов режимов
				 //Инициализация списка найденных каналов
	modeList = (UINT64*)malloc(lenList);
	memset(modeList, 0, lenList);
	//Чтение файла
	data = dataread(path);
	//Определение количества слов в канале
	numword = (uint)floor(fsize * 8 / (numorder));
	// Формирование массива значений
	// Получение указателя на массив слов канала
	wordsChan = getValues(data);
	free(data);
	// Поиск каналов режимов
	for (uint i = 1; i < (numword - 2); i++)
	{
		// Медианная фильтрация
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
	//Определение количества найденных режимов
	if (numModes > minNumMode && numModes < maxNumMode)
		return(true);
	else
		return(false);
}

/*Проверка входных параметров*/
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
	fdiskr = 100;//Частота дискретизации канала в Гц
	timeIntrvl = 1.0;//Минимальное временя работы в одном режиме
	numorder = 16;//Количество разрядов канала
	minNumMode = 3;//Минимальное количество идентифицированных режимов
	maxNumMode = 17;//Максимальное количество идентифицированных режимов
	numword = 0;//Количество отсчетов
	fsize = 0;//Размер файла
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

