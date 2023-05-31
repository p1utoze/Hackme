function checker()
{
    let a = document.getElementById("check_in");
    let b = document.getElementById("check_out");
    if (a.checked || b.checked)
        return true
    return false
}