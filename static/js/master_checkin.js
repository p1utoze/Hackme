function validform() {
    var a = document.forms["my-form"]["teamCode"].value;
    var b = document.forms["my-form"]["UID"].value;
    var c = document.forms["my-form"]["firstName"].value;
    var d = document.forms["my-form"]["lastName"].value;
    var e = document.forms["my-form"]["gender"].value;
    var f = document.forms["my-form"]["college"].value;
    var g = document.forms["my-form"]["phNo"].value;
    var h = document.forms["my-form"]["email"].value;
    var i = document.forms["my-form"]["teamName"].value;
    var j = document.forms["my-form"]["projectTracks"].value;

    data = {
        "teamCode": a,
        "UID": b,
        "firstName": c,
        "lastName": d,
        "gender": e,
        "college": f,
        "phNo": g,
        "email": h,
        "teamName": i,
        "projectTracks": j}

    console.log(data);

    if (a==null || a=="")
    {
        alert("Please Enter Your Full Name");
        return false;
    }else if (b==null || b=="")
    {
        alert("Please Enter Your Email Address");
        return false;
    }else if (c==null || c=="")
    {
        alert("Please Enter Your Username");
        return false;
    }else if (d==null || d=="")
    {
        alert("Please Enter Your Permanent Address");
        return false;
    }else if (e==null || e=="")
    {
        alert("Please Enter Your NID Number");
        return false;
    }
    else if (f==null || f=="")
    {
        alert("Please Enter Your NID Number");
        return false;
    }
    else if (g==null || g=="")
    {
        alert("Please Enter Your NID Number");
        return false;
    }
    else if (h==null || h=="")
    {
        alert("Please Enter Your NID Number");
        return false;
    }
    else if (i==null || i=="")
    {
        alert("Please Enter Your NID Number");
        return false;
    }
    else if (j==null || j=="")
    {
        alert("Please Enter Your NID Number");
        return false;
    }
    fetch('https://aventus-hackaventus.b4a.run/register/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(data)
    })
        .then(response => response.json())
  .then(data => {
    console.log(data);
  })
  .catch(error => {
    console.error('Error:', error);
  });
    return true;

}
