var slideIndex=1;
var click=0;
var time1;

function plusSlides(n)
{
	click=1;
	showSlides(slideIndex+=n);
}

function currentslide(n)
{
	click=1;
	showSlides(slideIndex=n);
}

function showSlides(n)
{
	var slide=document.getElementsByClassName("singleslide");
	var bubble=document.getElementsByClassName("dot");

	if(n>slide.length)
	{
		slideIndex=1;
	}
	if(n<1)
	{
		slideIndex=slide.length;
	}

	for(var i=0;i<slide.length;i++)
	{
		slide[i].style.display="none";
		bubble[i].className=bubble[i].className.replace(" active","");
	}

	slide[slideIndex-1].style.display="block";
	bubble[slideIndex-1].className+=" active";
	if(click==0)
  		time1=setTimeout(function(){showSlides(slideIndex+=1);},4000);
  	else if(click==1)
    	 click=0;
} 



// load view image to slideshow
 var loadFile = function(event) {
	    var output = document.getElementsByClassName("slidimg");
	    output[slideIndex-1].src = URL.createObjectURL(event.target.files[0]);
		click=1;	  
	    showSlides(slideIndex);
	};


function stoptime()
{
	clearTimeout(time1);
	
}

function starttime()
{
	if(click==0)
	showSlides(slideIndex);
}

// load view image to profile pic
 var loadFile1 = function(event) {
	    var output = document.getElementsByClassName("profilepic");
	    output[0].src = URL.createObjectURL(event.target.files[0]);
	};

