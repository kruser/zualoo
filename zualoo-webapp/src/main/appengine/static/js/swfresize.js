//Source adapted from sample found at - http://www.alistapart.com/articles/fontresizing/
function init()  
{
   var iBase = TextResizeDetector.addEventListener(onFontResize,null);
}
//id of element to check for and insert control
TextResizeDetector.TARGET_ELEMENT_ID = 'doc3';
//function to call once TextResizeDetector has init'd
TextResizeDetector.USER_INIT_FUNC = init;

/*
Copyright (c) 2006 Niqui Merret. 
http://niquimerret.com

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/
var lastSize = null;

function onFontResize(e,args) {
	lastSize = (lastSize == null)?args[0].iBase:lastSize;
	var newSize = (args[0].iSize == 0)?1:args[0].iSize;
	var sizeDiff = newSize/lastSize;
	var resizableswf = document.getElementById('example');
	if(resizableswf){
		//alert("WIDTH: " + parseFloat(resizableswf.offsetWidth));
		var newWidth = (parseFloat(resizableswf.offsetWidth)*parseFloat(sizeDiff))+"px";
		var newHeight = (parseFloat(resizableswf.offsetHeight)*parseFloat(sizeDiff))+"px";

		// Aral: If the new width is larger than the maxWidth, adjust the maxWidth accordingly
		// (This is necessary when using maxWidth along with a set height to make a SWF 
		// sit in a DIV and resize automatically when the page is resized).
		//alert ("w: " + newWidth + ", mW: " + resizableswf.style.maxWidth);
		if (newWidth > resizableswf.style.maxWidth)
			resizableswf.style.maxWidth = newWidth;
			
		resizableswf.style.width = newWidth;
		resizableswf.style.height = newHeight;
	}

	lastSize = newSize;
}