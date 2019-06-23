#include <Python.h>

static char module_docstring[] = "C extension to fetch an item from a nested structure made out of "
    "dictionaries and/or lists. "
    "Can reduce the time spent retrieving items from nested structures resulted after de-serializing JSON content "
    "or other nested structures.";

static char getp_docstring[] = "get an item from a nested structure mad out of dictionaries or/and lists"
    ":param nested_input (Required) - represents the nested input from which the item should be retrieved "
    "must be a dictionary or a list"
    ":param path (Required) - path to the item in the nested structure - composed using '.' "
    "separator by default between keys names and using integers for list indexes"
    ":param separator (Optional) - separator used for building the path, must be a unicode character: (Default: '.')"
    ":param default_value (Optional) - default value in case the path does not exist: (Default: None)"
    ":return PyObject"
    ":raises DictPathError - returns exception when invalid values have been provided in the inputs";

static PyObject *DictPathError;

static PyObject *get_from_path(PyObject *self, PyObject *args)
{
    /* Build the output tuple */
    //

    PyObject *nested_input;
    PyObject *path;
    PyObject *separator=PyUnicode_FromString(".");
    PyObject *default_value=Py_None;

    if (PyArg_ParseTuple(args, "OO|OO", &nested_input, &path, &separator, &default_value)) {
        if (!PyDict_Check(nested_input) && !PyList_Check(nested_input)) {
                PyErr_SetString(PyExc_TypeError, "nested_input must be a dictionary or a list");
                return NULL;
        }

        if (!PyUnicode_Check(path)) {
                PyErr_SetString(PyExc_TypeError, "path must be an unicode string");
                return NULL;
        }

        if (separator && !PyUnicode_Check(separator)) {
                PyErr_SetString(PyExc_TypeError, "separator must be an unicode string");
                return NULL;
        }
    } else {
        PyErr_SetString(PyExc_TypeError, "invalid arguments");
        return NULL;
    }

    PyObject *keys = PyUnicode_Split(path, separator, -1);
    PyObject *result = nested_input;

    for(int i=0; i<PyList_GET_SIZE(keys); i++){
        PyObject *key = PyList_GetItem(keys, i);

        if (PyDict_Check(result) && PyDict_Contains(result, key)){
            result = PyDict_GetItem(result, PyList_GetItem(keys, i));
        }
        else if (PyDict_Check(result)
                    && Py_UNICODE_ISDECIMAL(*PyUnicode_AS_UNICODE(key))
                    && PyDict_Contains(result, PyLong_FromLong(Py_UNICODE_TODECIMAL(*PyUnicode_AS_UNICODE(key))))){
            result = PyDict_GetItem(result, PyLong_FromLong(Py_UNICODE_TODECIMAL(*PyUnicode_AS_UNICODE(key))));
        }
        else if (PyList_Check(result)
                    && Py_UNICODE_ISDECIMAL(*PyUnicode_AS_UNICODE(key))
                    && Py_UNICODE_TODECIMAL(*PyUnicode_AS_UNICODE(key)) < PyList_GET_SIZE(result)) {
            long path_index = Py_UNICODE_TODECIMAL(*PyUnicode_AS_UNICODE(key));
            result = PyList_GetItem(result, PyLong_AsSize_t(PyLong_FromLong(path_index)));
        } else return default_value;
    }

    return Py_BuildValue("O", result);
}

static PyMethodDef module_methods[] = {
    {"getp", get_from_path, METH_VARARGS, getp_docstring},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef upath_module = {
    PyModuleDef_HEAD_INIT,
    "upath",   /* name of module */
    module_docstring, /* module documentation, may be NULL */
    -1,       /* size of per-interpreter state of the module,
                 or -1 if the module keeps state in global variables. */
    module_methods,
};

PyMODINIT_FUNC PyInit_upath(void)
{
    PyObject *m;

    m = PyModule_Create(&upath_module);

    DictPathError = PyErr_NewException("upath.error", NULL, NULL);
    Py_INCREF(DictPathError);
    PyModule_AddObject(m, "error", DictPathError);
    return m;
}