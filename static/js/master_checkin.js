function validform() {

    var a = document.forms["my-form"]["Team Code"].value;
    var b = document.forms["my-form"]["UID"].value;
    var c = document.forms["my-form"]["First Name"].value;
    var d = document.forms["my-form"]["Last Name"].value;
    var e = document.forms["my-form"]["Gender"].value;
    var f = document.forms["my-form"]["College"].value;
    var g = document.forms["my-form"]["Ph. No"].value;
    var h = document.forms["my-form"]["Email"].value;
    var i = document.forms["my-form"]["Team Name"].value;
    var j = document.forms["my-form"]["Project Tracks"].value;

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
    return true;

}