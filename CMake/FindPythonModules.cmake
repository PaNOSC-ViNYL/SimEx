function(find_python_module module)
    set (PYTHON_EXECUTABLE python)
    execute_process(COMMAND "${PYTHON_EXECUTABLE}" "-c" 
	"import ${module};"
	RESULT_VARIABLE _${module}_status 
	ERROR_QUIET)
	if(NOT _${module}_status)
         message ("-- Python module ${module} is found")				
	else(NOT _${module}_status)
	    if(ARGC GREATER 1 AND ARGV1 STREQUAL "REQUIRED")
	        message (FATAL_ERROR "-- Python module ${module} is not found")
	    else()
	        message ("-- Python module ${module} is not found")
	    endif()
    endif(NOT _${module}_status)
endfunction(find_python_module)

