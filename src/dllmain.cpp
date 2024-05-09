#include <Extension_Interface.h>
#include <YYRValue.h>
#include <Constants.h>

YYRunnerInterface gs_runnerInterface;
YYRunnerInterface* g_pYYRunnerInterface;

YYEXPORT void YYExtensionInitialise(const struct YYRunnerInterface* _pFunctions, size_t _functions_size)
{
	 //copy out all the functions 
	memcpy(&gs_runnerInterface, _pFunctions, sizeof(YYRunnerInterface));
	g_pYYRunnerInterface = &gs_runnerInterface;

	if (_functions_size < sizeof(YYRunnerInterface)) {
		DebugConsoleOutput("ERROR : runner interface mismatch in extension DLL\n ");
	} // end if

	DebugConsoleOutput("YYExtensionInitialise CONFIGURED \n ");
}

YYEXPORT void SimpleDesktopExample_Test(RValue& Result, CInstance* selfinst, CInstance* otherinst, int argc, RValue* arg)
{
	Result.kind = VALUE_REAL;
	Result.val = YYGetReal(arg, 0);
}

YYEXPORT void SimpleDesktopExample_ReturnString(RValue& Result, CInstance* selfinst, CInstance* otherinst, int argc, RValue* arg)
{
	DebugConsoleOutput("SimpleDesktopExample_ReturnString \n");
	YYCreateString(&Result, "Hello World");
}

double val = 0;
YYEXPORT void SimpleDesktopExample_ReturnDouble(RValue& Result, CInstance* selfinst, CInstance* otherinst, int argc, RValue* arg)
{
	double inc = YYGetReal(arg, 0);

	val += inc;

	Result.kind = VALUE_REAL;
	Result.val = val;
}

YYEXPORT void SimpleDesktopExample_AsyncCallback(RValue& Result, CInstance* selfinst, CInstance* otherinst, int argc, RValue* arg)
{
	int map = CreateDsMap(0,0);
	DsMapAddString(map, "type", "SimpleDesktopExample_AsyncCallback");
	DsMapAddDouble(map, "double", val);
	DsMapAddString(map, "string", "Hello World");

	CreateAsyncEventWithDSMap(map, ev_async_social);
}

// YYEXPORT void SimpleDesktopExample_EchoStruct(RValue& Result, CInstance* selfinst, CInstance* otherinst, int argc, RValue* arg)
// {
// 	RValue* pV = &(arg[0]);

// 	COPY_RValue(&Result, pV);
// 	FREE_RValue(pV);
// }

YYEXPORT void SimpleDesktopExample_ReturnStruct(RValue& Result, CInstance* selfinst, CInstance* otherinst, int argc, RValue* arg)
{
	RValue Struct = { 0 };
	YYStructCreate(&Struct);

	YYStructAddDouble(&Struct, "double", val);
	YYStructAddString(&Struct, "string", "YoYoGames X Opera");

	COPY_RValue(&Result, &Struct);
	FREE_RValue(&Struct);
}
