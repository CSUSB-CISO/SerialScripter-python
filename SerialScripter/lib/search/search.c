#include <Python.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    int* matrix;
    size_t rows;
    size_t cols;
} Matrix;

Matrix create_matrix(size_t rows, size_t cols) {
    Matrix mat;
    mat.rows = rows;
    mat.cols = cols;
    mat.matrix = (int*) calloc(rows * cols, sizeof(int));
    return mat;
}

void destroy_matrix(Matrix mat) {
    free(mat.matrix);
}

int matrix_get(Matrix mat, size_t row, size_t col) {
    return mat.matrix[row * mat.cols + col];
}

void matrix_set(Matrix mat, size_t row, size_t col, int value) {
    mat.matrix[row * mat.cols + col] = value;
}

int maximum(int a, int b) {
    return a > b ? a : b;
}

double ratio(const char* str1, const char* str2) {
    size_t len1 = strlen(str1);
    size_t len2 = strlen(str2);

    if (len1 == 0 || len2 == 0) {
        return 0.0;
    }

    Matrix mat = create_matrix(len1 + 1, len2 + 1);

    for (size_t i = 0; i <= len1; i++) {
        matrix_set(mat, i, 0, 0);
    }

    for (size_t j = 0; j <= len2; j++) {
        matrix_set(mat, 0, j, 0);
    }

    int match, insert, delete, cost;

    for (size_t i = 1; i <= len1; i++) {
        for (size_t j = 1; j <= len2; j++) {
            match = matrix_get(mat, i-1, j-1) + (str1[i-1] == str2[j-1] ? 1 : 0);
            insert = matrix_get(mat, i, j-1);
            delete = matrix_get(mat, i-1, j);
            cost = maximum(match, maximum(insert, delete));
            matrix_set(mat, i, j, cost);
        }
    }

    int matches = matrix_get(mat, len1, len2);
    double sim = (double)matches / (double)maximum(len1, len2);

    destroy_matrix(mat);

    return sim;
}

static PyObject* find_matches(PyObject* self, PyObject* args) {
    PyObject* dict_list;
    const char* search_str;
    double match_ratio;

    if (!PyArg_ParseTuple(args, "Osd", &dict_list, &search_str, &match_ratio)) {
        return NULL;
    }

    if (!PyList_Check(dict_list)) {
        PyErr_SetString(PyExc_TypeError, "Expected a list object");
        return NULL;
    }

    PyObject* matches = PyList_New(0);
    

    Py_ssize_t list_size = PyList_Size(dict_list);
    
    for (int i = 0; i < list_size; i++) {
        PyObject* dict_obj = PyList_GetItem(dict_list, i);

        if (!PyDict_Check(dict_obj)) {
            PyErr_SetString(PyExc_TypeError, "Expected a dictionary object");
            return NULL;
        }

        Py_ssize_t pos = 0;
        PyObject* key;
        PyObject* value;
        while (PyDict_Next(dict_obj, &pos, &key, &value)) {
            const char* key_str = PyUnicode_AsUTF8(key);
            if (strcmp(key_str, "name") == 0) {
                char* name_str = PyUnicode_AsUTF8(value);
                double sim = ratio(name_str, search_str);
                if (sim >= match_ratio) {
                    PyObject* result = PyDict_GetItem(dict_obj, PyUnicode_FromString("Host"));
                    char* str = PyUnicode_AsUTF8(result);
                    PyList_Append(matches, PyUnicode_FromString(str));

                    Py_DECREF(result);
                }
            }
            else {
                if (PyUnicode_Check(value)) {
                    char* str = PyUnicode_AsUTF8(value);
                    double sim = ratio(str, search_str);
                    if (sim >= match_ratio) {
                        PyObject* result = PyDict_GetItem(dict_obj, PyUnicode_FromString("Host"));
                        char* str = PyUnicode_AsUTF8(result);
                        PyList_Append(matches, PyUnicode_FromString(str));

                        Py_DECREF(result);
                    }
                }
            }
        }
    }

    return matches;
}


static PyMethodDef search_methods[] = {
    {"find_matches", find_matches, METH_VARARGS, "Find matching incidents in a list."},
    {NULL, NULL, 0, NULL}
};

static struct PyModuleDef search_module = {
    PyModuleDef_HEAD_INIT,
    "search",
    "Example module that uses C code",
    -1,
    search_methods
};

PyMODINIT_FUNC PyInit_search(void) {
    printf("Initializing search\n");
    PyObject* m = PyModule_Create(&search_module);
    if (m == NULL) {
        return NULL;
    }
    printf("Initialized search\n");
    return m;
}

