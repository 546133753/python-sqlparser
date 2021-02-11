//#include "node_visitor.h"
#include "gsp_base.h"
#include "gsp_node.h"
#include "gsp_list.h"
#include "gsp_sourcetoken.h"
#include "gsp_sqlparser.h"
#include <stdlib.h>
#include <Python.h>
#include <structmember.h>

#include "Parser.h"
#include "Statement.h"
#include "Node.h"
#include "ENodeType.h"

#if PY_MAJOR_VERSION >= 3
static PyModuleDef SqlParserModule = {
    PyModuleDef_HEAD_INIT,
    .m_name = "sqlparser",
    .m_doc = "Bridge between python and sqlparser",
    .m_size = -1
};

PyMODINIT_FUNC PyInit_sqlparser(void)
{
    PyObject *m;

    if (PyType_Ready(&ParserType) < 0)
        return NULL;

    // initialize module
    m = PyModule_Create(&SqlParserModule);
    if (m == NULL) return NULL;

    // Initialize our custom types
	Parser_init_type(m);
	Node_init_type(m);
	Statement_init_type(m);
	Enum_init_type(m);
	return m;
}
#else
// Module functions
static PyMethodDef BridgeMethods[] =
{
     {NULL, NULL, 0, NULL}
};
 
PyMODINIT_FUNC
initsqlparser(void)
{
	PyObject *m;

	// initialize module
    m = Py_InitModule3("sqlparser", BridgeMethods, "Bridge between python and sqlparser");
	 
	if (m == NULL) return;
	
	// Initialize our custom types
	Parser_init_type(m);
	Node_init_type(m);
	Statement_init_type(m);
	Enum_init_type(m);
}
#endif