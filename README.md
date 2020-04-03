
<img src="https://user-images.githubusercontent.com/48054293/53554351-ce33f200-3b3f-11e9-9bca-560c1cd5d115.jpg" width="480" height="100">
<br />
<br />

#### What is EIDEGraphics
a ver enlace[enlace](https://github.com/Vicente-Francisco/EIDEGraphics/blob/master/Gravity_pH_datasheet.svg)

EIDEGraphics is a python library that helps showing numeric values in big characters, in the form of gauge indicators and/or as LED's bars. User may select every indicator size and position inside the window. 
<br />
<br />

<p align="center">
  <img src="https://user-images.githubusercontent.com/48054293/53554427-ff142700-3b3f-11e9-9f86-146dffdbfa57.png" width="650"   height="440">
  </p>
  <p align="center">
  EIDEGraphis library powered user synoptic.
</p>
<br />
<br />

Indicators are highly parametrizable, so quite different looks of every indicator may be achieved. Parametrization is made by means of plain text files and graphic (‘jpg’, ‘bmp’, …) files; no coding is needed at all. Seven different indicators are pre-configured and ready to use.


<p align="center">
  <img src="https://user-images.githubusercontent.com/48054293/53554387-e3a91c00-3b3f-11e9-80ae-563937bcb762.png" width="710"   height="480">
  </p>
  <p align="center">
EIDEGraphis car like panel.
  </p>



The whole window background is also user selectable so by using EIDEGraphics one can build synoptics or big panels showing what the user needs in many different ways. EIDEGraphics downloads itself with a set of examples to guide the user and to show EIDEGraphics capabilities.

EIDEGraphics is written in Python and makes an extensive use of the ‘pygame’ library. EIDEGraphics is OPEN SOURCE.

### EIDEGraphics installation
There are many ways of using EIDEGraphics:
1) Newcomers are encouraged to download the whole library (../EIDEGraphics/EIDEGraphics/..) and copy it where appropriate (‘Desktop’, ‘Downloads’ folder, ...). EIDEGraphics native code includes the necessary instructions to adapt paths to code and data so examples are directly executable from its own ‘test’ folder (‘test.py’)[^1].
2) An intermediate user may download just the code (../EIDEGraphics/) and ‘PROJECTS_N_EXAMPLES’ folder and address it as a library. User may adhere to the proposed folders layout to add his/her own project or -EIDEGraphics- evaluation module.
3) An expert user may just download the code (../EIDEGraphics/) and place it wherever appropriate. This case the user has to manage the paths to access the library[^2].
4) EIDEGraphics is OPEN SOURCE and conceived such a way that indicators with added features may be added with ease. Code is troughfully commented so an experienced python programmer will understand easily how each module operates[^3].

[^1]: A basic knowledge of python is needed to use the library.
[^2]: EIDEGraphics Pypi inclusion is in preparation.
[^3]: An ‘User manual’ is in preparation; it will be published in fascicles, being the most useful chapters (i.e. ‘Built in indicators usage’, ‘Coding a new display type’) released independently. 



<p align="center">
  <img src="https://user-images.githubusercontent.com/48054293/53554403-f02d7480-3b3f-11e9-9faf-e2eea799b3f2.png" width="800"   height="550">

</p>
<p align="center">
 EIDEGraphics 'built in' indicators (ready to use)
  
</p>


### Examples.
EIDEGraphics includes as many examples as subfolders in the ‘PROJECTS_N_EXAMPLES’ folder. Just modify (../EIDEGraphics/EIDEGraphics/)‘EIDESystem.txt' 'project' field entering the folder name you want to run and launch ‘test.py’.



<p align="center">
  <img src="https://user-images.githubusercontent.com/48054293/53554403-f02d7480-3b3f-11e9-9faf-e2eea799b3f2.png" width="400"   height="275">

  <img src="https://user-images.githubusercontent.com/48054293/53554435-089d8f00-3b40-11e9-8aed-3fd54e8108c4.png" width="400"   height="275">
  </p>

<p align="center">
EIDEGraphis powered examples.
  </p>

### Prerequisites.
Python 2.7
pygame 1.9.1       


### License.
Copyright (c) 2019. Vicente Francisco (mafg558128m@gmail.com)
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
