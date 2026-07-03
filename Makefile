UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Darwin)
	LIB := build/libpicnic.dylib
	DYNLIB_FLAG := -dynamiclib
else
	LIB := build/libpicnic.so
	DYNLIB_FLAG := -shared
endif

.PHONY: build verify test run clean

build: $(LIB)

$(LIB): generated/picnic_kernel.s
	mkdir -p build
	clang $(DYNLIB_FLAG) -o $(LIB) generated/picnic_kernel.s

verify: build
	python3 scripts/verify_angl_examples.py

test: verify
	python3 tests/test_adapter.py

run: build
	python3 app/server.py

clean:
	rm -rf build
