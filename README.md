# General info

This toolbox is made of two main component

1. The NIST Lithography toolbox made by Rob Illic at NIST and using a java backend for easy creation of primitive or polygons into gds.
2. A python layer created by me for very easy user interfacing to generated dense layout of differnet microring resonator

# Installing the NIST nanolithography toolbox

Here I would only discuss the UNIX way to install, it no idea how to do on Windows. Should be similar but I invite you to look at [Rob's toolbox manual](CNSTnanoToolboxV2019.05.01/CNSTNanolithographyToolboxV2016.10.01.pdf) if needed

1. Download and install the version 8 of the [Java Runtime Environment](https://www.oracle.com/java/technologies/javase/javase8u211-later-archive-downloads.html).
2. If you are on a Linux machine, make sure that you are indeed using this version of java
   - list all version of java install using `update-java-alternatives --list`
   - change if needed which version you are using through `sudo update-alternatives --config java`
   - You may need to reboot.
   - Open the [NIST toolbox ui](CNSTnanoToolboxV2019.05.01/CNSTspecialScriptsV2019.05.01.jar) to check if it works, usually through a command line such that `java -jar <jarFile>`

# Installing the pyNISTtoolbox layer

You shouldn't have much to do here hopefully. Either you know you won't touch much the toolbox and you can install it system-wide through

```
python setup.py install
```

Note: you may need to use `python3` depending on your environment. Note: you may want to create a virtual environment first

If you plan on tweaking it, I recomand to add the NISTgenerator package to your python path manually as described in the examples

# Using the pyNISTtoolbox

## Addint the NISTgenerator to you path

In case you are tweaking the package a lot, it is easier to put it in a path that is more user friendly than the standard `site-packaged` such that:

```
import os, sys
parFile = os.path.expanduser(r"/Users/greg/Documents/Nanofab/PatternDesign/")
if not parFile in sys.path:
    sys.path.insert(-1, parFile)
```

## Defining global parameters

Defining a set of parameters that are global for the chip, all parameter should be straighforward to understand. Both a `Global Parameter` and a `Cell` dictionary must be defined

```
GlobalParams = dict(
    resist="positive",
    Wchip=2500,
    Hchip=10000,
    layer_ring=1,
    layer_waveguide=1,
    layer_label=1,
    device_layer=1,
    photomask_layer=1,
)
Cells = dict(ncell=-1, cell_type=[], param=[], YSHIFT=[])
```

## Defining the designs by block
