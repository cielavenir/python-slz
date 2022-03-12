#include <pybind11/pybind11.h>

extern "C" {
#include "libslz/src/slz.h"
struct slz_stream *slz_alloc();
void slz_free(struct slz_stream *s);
}

#if defined(_WIN32) || (!defined(__GNUC__) && !defined(__clang__))
#define ssize_t Py_ssize_t
#endif

namespace py = pybind11;
using namespace pybind11::literals;

class slz_compressobj{
    slz_stream strm;
    slz_stream *pstrm;
    std::string out;
    int outsize;
public:
    slz_compressobj(int level=1, int format=SLZ_FMT_DEFLATE): outsize(0){
printf("pypypy %d\n",sizeof(slz_stream));
#if defined(_WIN32) || (!defined(__GNUC__) && !defined(__clang__))
        pstrm = slz_alloc();
#else
        pstrm = &strm;
#endif
        slz_init(pstrm, level, format);
    }
    ~slz_compressobj(){
#if defined(_WIN32) || (!defined(__GNUC__) && !defined(__clang__))
        slz_free(pstrm);
#endif
    }
    py::bytes compress(const py::bytes &obj){
		fprintf(stderr, "0\n");fflush(stderr);
		fprintf(stderr, "iii_%d\n", py::len(obj));fflush(stderr);
        int tempoutsize = py::len(obj)+py::len(obj)/16;
        if(outsize < tempoutsize){
            outsize = tempoutsize;
            out.resize(outsize);
        }
        //out.resize(tempoutsize);
        size_t written = 0;
        {
			fprintf(stderr, "1\n");fflush(stderr);
            char *buffer = nullptr;
            ssize_t length = 0;
            PYBIND11_BYTES_AS_STRING_AND_SIZE(obj.ptr(), &buffer, &length);
            //py::gil_scoped_release release;
			fprintf(stderr, "2\n");fflush(stderr);
            written = slz_encode(pstrm, &out[0], buffer, length, 1);
  //written = slz_finish(pstrm, &out[0]);
      }
        //out.resize(written);
		fprintf(stderr, "ooo_%d\n", written);fflush(stderr);
        return py::bytes(out.data(), written);
    }
    py::bytes flush(){
		fprintf(stderr, "f0\n");fflush(stderr);
        int tempoutsize = 12;
        if(outsize < tempoutsize){
            outsize = tempoutsize;
            out.resize(outsize);
        }
        //out.resize(tempoutsize);
        size_t written = 0;
        {
			fprintf(stderr, "f1\n");fflush(stderr);
            //py::gil_scoped_release release;
			fprintf(stderr, "f2\n");fflush(stderr);
            written = slz_finish(pstrm, &out[0]);
        }
        //out.resize(written);
        return py::bytes(out.data(), written);
    }
};

PYBIND11_MODULE(slz, m){
    py::class_<slz_compressobj, std::shared_ptr<slz_compressobj> >(m, "compressobj")
    .def(py::init<int, int>(), "level"_a=1, "format"_a=int(SLZ_FMT_DEFLATE))
    .def("compress", &slz_compressobj::compress,
     "obj"_a
    )
    .def("flush", &slz_compressobj::flush)
    ;

    m.attr("SLZ_FMT_GZIP") = int(SLZ_FMT_GZIP);
    m.attr("SLZ_FMT_ZLIB") = int(SLZ_FMT_ZLIB);
    m.attr("SLZ_FMT_DEFLATE") = int(SLZ_FMT_DEFLATE);
}
