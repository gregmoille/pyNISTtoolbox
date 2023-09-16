# General info

This toolbox is made of two main component

1. The NIST Lithography toolbox made by Rob Illic at NIST and using a java backend for easy creation of primitive or polygons into gds. **That is pretty much working for sure and refer to the [Rob's tool page](https://www.nist.gov/services-resources/software/cnst-nanolithography-toolbox) for more information**
2. A python layer created by me for very easy user interfacing to generated dense layout of differnet microring resonator. Well, here that's my contribution, and it may or may not work perfectly but so far it works sufficiently good enough.

I so not plan on creating new functionallity based on the community needed. Instead, I am sharing what I have developed throughout the years and used regularly for my own designs. Reach out if needed but I provide very limited support.

**In the idea of sharing with the community, if you create new functionality, create a pull requests please**

# Installing the NIST nanolithography toolbox

## Setting up the java environment

Here I would only discuss the UNIX way to install, it no idea how to do on Windows. Should be similar but I invite you to look at [Rob's toolbox manual](CNSTnanoToolboxV2019.05.01/CNSTNanolithographyToolboxV2016.10.01.pdf) if needed

1. Download and install the **Oracle** version 8 of the [Java Runtime Environment](https://www.oracle.com/java/technologies/javase/javase8u211-later-archive-downloads.html). (Note: OpenJava will not work_
2. If you are on a Linux machine, make sure that you are indeed using this version of java
   - list all version of java install using `update-java-alternatives --list`
   - change if needed which version you are using through `sudo update-alternatives --config java`
   - You may need to reboot.
   - Open the [NIST toolbox ui](CNSTnanoToolboxV2019.05.01/CNSTspecialScriptsV2019.05.01.jar) to check if it works, usually through a command line such that `java -jar <jarFile>`

## Setting up the variable for the toolbox

You will have to modify the [xml file](CNSTnanoToolboxV2019.05.01/CNSTdefaultValues.xml) that defined where all the path are for the java toolbox. In particular [line 64](https://github.com/gregmoille/pyNISTtoolbox/blob/d65660f7f812bbb7bc3dde72d425e5a79359e032/CNSTnanoToolboxV2019.05.01/CNSTdefaultValues.xml#L64) to defined where the CNST is placed in your system.

⚠︎ Note that [line 69](https://github.com/gregmoille/pyNISTtoolbox/blob/d65660f7f812bbb7bc3dde72d425e5a79359e032/CNSTnanoToolboxV2019.05.01/CNSTdefaultValues.xml#L69) should not be changed. It is essential to save the gds to `/opt/gds` for the python toolbox to work.
To this extend you may want to create a folder `sudo mkdir /opt/gds` which you set the property correctly `sudo chmod 777 /opt/gds`

# Installing the pyNISTtoolbox layer

You shouldn't have much to do here hopefully. Either you know you won't touch much the toolbox and you can install it system-wide through

```
python setup.py install
```

Note: you may need to use `python3` depending on your environment. Note: you may want to create a virtual environment first

If you plan on tweaking it, I recomand to add the NISTgenerator package to your python path manually as described in the examples

# Using the pyNISTtoolbox

## Adding the NISTgenerator to you path

In case you are tweaking the package a lot, it is easier to put it in a path that is more user friendly than the standard `site-packaged` such that:

```python
import os, sys
parFile = os.path.expanduser(r"/Users/greg/Documents/Nanofab/PatternDesign/")
if not parFile in sys.path:
    sys.path.insert(-1, parFile)
```

## Defining global parameters

Defining a set of parameters that are global for the chip, all parameter should be straighforward to understand. Both a `Global Parameter` and a `Cell` dictionary must be defined

```python
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

A single chip is defined by "Blocks", each block being looped through the parameter that are sets inside a dictionary. Every combination possible will be created with this type of nesting:

- Pulley length:
  - waveguide/ring gap:
    - Dimer gap:
      - Ring width:
        - Ring radius:
          - Bus waveguide width:
            - PhC inner ring modulation strength:
              - PhC ring modulation phase:

(i.e. if ring width and ring radius are varried, all the different ring radii will be next to each other with a fixed RW, and the RW is steped once the variation of RR is done)

Several Blocks can be defined, and they will be shifted by the parameter `top_shift` which is a loose thing to set

**⚠︎All dimnesioned are in micrometers!!⚠︎**

```python
Block = [
    dict(
        racetrack=True,
        heater=True,
        RR=23,
        Lrace=361,
        G=np.arange(300, 600.1, 100),
        RW=np.arange(800, 1000.1, 10),
        W=0.460,
        ypitch=10,
        xpitch=165,
        carriage_shift=20,
        Wtapper=0.2,
        xdec=180,
        Label="Rtrack Lc=361 Curve Cpl - 400GHz",
    ),
    dict(
        top_shift=1600,
        racetrack=True,
        heater=True,
        RR=23,
        Lrace=361,
        G=np.arange(300, 600.1, 100),
        RW=np.arange(1700, 2100.1, 25),
        W=0.460,
        ypitch=10,
        xpitch=165,
        carriage_shift=20,
        Wtapper=0.32,
        xdec=180,
        Label="Rtrack Lc=361 Curve Cpl - 400GHz ª • 1550nm pump",
    )
]
```

If multiple chips needs to be made, it is convenient to wrap the each `Block` list into another dictionary, index by the chip number. FOr instance

```python
Blocks = {}
Blocks[1] = [
    dict(
        RR=23,
        G=gregArange(250, 50, 600),
        RW=gregArange(800, 10, 920),
        W=gregArange(360, 100, 660),
        ypitch=9.5,
        xpitch=85,
        xdec=97,
        Label="RR=23 Strg Cpl",
    )
]

Blocks[2] = [copy(Blocks[1][0])]
Blocks[2][0].update(RR = 24)
```

## Generation of the chip

Several utilies are defined for the sake of simplicity to create the design and make them into a chip. Usually the standard ones are:

### Logfile

```python
NISTgenerator.Utils.LogFile(GlobalParams, block, Cells, design_number=index)
```

This create a log file in the `log` folder of the working directory

### Top Label

```python
NISTgenerator.ChipFeature.TopLabel(Cells, GlobalParams, block, data=label, design_number=index)
```

Create a top label for chip identification. This also create a QR code and can be disbaled

### Densed ring desing for Lignetec

```python
NISTgenerator.Ring.RingPulleyWgShifted(Cells, GlobalParams, Block, design_number=index)
```

This function let you create from the a single Block list the densed version of the Ligentec layout.

### Others that I will need to explain later

## CNST and GDS generation

The generation is split in two steps: creation of the cnst file through python, creation of the gds from the java tool box.

Hence, one need to first call the

```python
CNSTpath = os.path.expanduser(<PATH WHERe IT>r"CNSTnanoToolboxV2019.05.01/cnst_script_files/")
NISTgenerator.Builder.CreateCNST(
        Cells["cell_type"],
        Cells["param"],
        "DesignFilenName",
        yshift=Cells["YSHIFT"],
        CNSTpath=CNSTpath,
        top_cell_name=f"TOP",
        xdec=GlobalParams["Wchip"] / 2,
        ydec=GlobalParams["Hchip"],
        res=0.005,
    )
```

Please be adviced to change the `res` parameter accordingly to your fabrication process.

This will create a `DesignFilenName.cnst` in the `cnst` folder of your working directory.

To create the gds file, one would nee to use

```python
Gen.Builder.CreateGDS(
        GlobalParams["filename"],
        CNSTpath=CNSTpath,
        GDSpath=r"/opt/gds_files_created/",
        ToolBoxPath=CNSTpath.split("cnst_")[0],
        javaVers="CNSTspecialScriptsV2019.05.01.jar",
        removeRobCell=True,
        dogds=True,
        dcty=os.path.dirname(__file__),
    )
```

Which will create a `DesignFilenName.gds` in the `gds` folder of your working directory

## Generating multiple chips

When many chips (let's say 44), it becomes convenient to define all the parameter in separate files, define a dictionary of block for each chip, indexed by the chip number and run a loop for the gds generation

## Creating a Reticle
