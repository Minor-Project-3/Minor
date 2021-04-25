function dropdownFunction() {
    document.getElementById("droplist").classList.toggle("show");
  }
  
  // Close the dropdown if the user clicks outside of it
  window.onclick = function(e) {
    if (!e.target.matches('#dropbtn')) {
    var myDropdown = document.getElementById("droplist");
      if (myDropdown.classList.contains('show')) {
        myDropdown.classList.remove('show');
      }
    }
  }

  //read more 

  function myFunction() {
    var dots = document.getElementById("dots");
    var moreText = document.getElementById("more");
    var btnText = document.getElementById("myBtn");
  
    if (dots.style.display === "none") {
      dots.style.display = "inline";
      btnText.innerHTML = "read more";  
      moreText.style.display = "none";
    } else {
      dots.style.display = "none";
      btnText.innerHTML = "read less"; 
      moreText.style.display = "inline";
    }
  }




  var granimInstance = new Granim({
    element: '#logo-canvas',
    direction: 'left-right',
    states : {
        "default-state": {
            gradients: [
                ['#EB3349', '#F45C43'],
                ['#FF8008', '#FFC837'],
                ['#4CB8C4', '#3CD3AD'],
                ['#24C6DC', '#514A9D'],
                ['#FF512F', '#DD2476'],
                ['#DA22FF', '#9733EE']
            ],
            transitionSpeed: 2000
        }
    }
});


// change header icon text color and image when mouse over it
function headerchange(check)
{
	if(check==1)
	{
		var text=document.getElementById('p1').style.color="white";
		var img=document.getElementById('home').src="../static/images/home-hover.png";
	}
	else if(check==2)
	{
		var text=document.getElementById('p2').style.color="white";
		var img=document.getElementById('profile').src="../static/images/profile-hover.png";
	}
	else if(check==3)
	{
		var text=document.getElementById('p3').style.color="white";
		var img=document.getElementById('following').src="../static/images/foloowing-hover.png";
	}
	else if(check==4)
	{
		var text=document.getElementById('p4').style.color="white";
		var img=document.getElementById('notification').src="../static/images/notification-hover.png";
	}
}


// change header icon text color and image to origin when mouseout
function headerorigin(check)
{
	if(check==1)
	{
		var text=document.getElementById('p1').style.color="black";
		var img=document.getElementById('home').src="../static/images/home.png";
	}
	else if(check==2)
	{
		var text=document.getElementById('p2').style.color="black";
		var img=document.getElementById('profile').src="../static/images/profile.png";
	}
	else if(check==3)
	{
		var text=document.getElementById('p3').style.color="black";
		var img=document.getElementById('following').src="../static/images/foloowing.png";
	}
	else if(check==4)
	{
		var text=document.getElementById('p4').style.color="black";
		var img=document.getElementById('notification').src="../static/images/notification.png";
	}
}


function onbuttoncolor()
 {
 	var on=document.getElementById("imgbttn");
 	on.style.backgroundColor = "#009688";
 	on.style.color="white";
 }

// chaging imagebutton color on hover out
 function outbuttoncolor()
 {
 	var out=document.getElementById("imgbttn");
 	out.style.backgroundColor = "white";
 	out.style.color="black";
 }




 var society=0;
// change logo of connect when click
function changelogo(connectID)
{
	var connect=document.getElementById(connectID);
	// alert("hello");
	// connect.style.width="0px";
     connect.innerHTML="";
     // connect.innerHTML="&#x2714";
    

  connect.style.pointerEvents="none";
  connect.style.border= "8px solid #f3f3f3";
  connect.style.borderRadius="50%";
  connect.style.borderTop= "8px solid #009688";
  connect.style.borderBottom= "8px solid #009688";
  connect.style.width= "12px";
  connect.style.height= "12px";
  connect.style.margin="0px";
  connect.style.animation= "spin 2s linear 2";
  connect.style.marginRight="18px";
  // change logo after 3 sec
  setTimeout(function(){
  	  connect.style.animationPlayState= "paused";
	  connect.style.border= "0px";
	  connect.style.borderRadius="0px";
	  connect.style.borderTop= "0px";
	  connect.style.borderBottom= "0px";
	  connect.style.animation= "";
	  connect.style.margin="0px";
	  connect.style.padding="0px";
	  connect.style.marginRight="30px";
	  connect.innerHTML="&#x2714";
	  connect.style.color="#009688";
	  connect.style.fontSize="28px"; 
	  connect.style.pointerEvents="none";
	  
	  // increasing no. of society when clicked on connect
	  society=society+1;

	  var nooffollowers=document.getElementById("nofollowers");
	  var place=parseInt(nooffollowers.innerHTML)+1;
	  nooffollowers.innerHTML=place;}, 3000);
	
}