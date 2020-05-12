# MakeFortDep
Small Python3 script to build fortran dependencies. Only supports USE statement for now. Creates invisible (.name.d) dependecy file for each source file .f90.

Can be embedded into the project through the call from the Makefile.

**Example** (will put all the dependecy rules into one file -> .depends) **:**
```
FSRC = $(wildcard *.f90)
FDEPS = $(patsubst %.f90,.%.d,$(FSRC))

DEP=.depends
include $(DEP)
$(DEP): $(FDEPS)
	cat $(FDEPS) > $(DEP)

$(FDEPS): $(FSRC)
	$(HOME)/./make_dep.py -p $(SRC) -d $(SRC) -o $(LIB)
```

Specify path to the source files (.f90) after -p, where the dependecy files should be stored after -d, where the object files are stored after -o.
