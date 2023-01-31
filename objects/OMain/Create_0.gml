var _test = SimpleDesktopExample_Test(7);
show_debug_message(_test);

var _string = SimpleDesktopExample_ReturnString();
show_debug_message(_string);

repeat (5)
{
	var _double = SimpleDesktopExample_ReturnDouble(1);
	show_debug_message(_double);
}

SimpleDesktopExample_AsyncCallback();

var _struct = SimpleDesktopExample_ReturnStruct();
show_debug_message(_struct);
