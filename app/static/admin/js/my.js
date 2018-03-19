function validInitScore(str) {
    // 0 或者非 0 开头的数（1~4）位
    var myreg = /^(0|[1-9]\d{0,8})$/;
    if(!myreg.test(str)) {
        return false;
    }
    return true;
}


function validInitFund(str) {
    // 0 或者非 0 开头的数（1~4）位
    var myreg = /^(0|[1-9]\d{0,8})$/;
    if(!myreg.test(str)) {
        return false;
    }
    return true;
}


function validScore(str) {
    // 非0开头的数（1~4）位
    var myreg = /^([1-9]\d{0,3})$/;
    if(!myreg.test(str)) {
        return false;
    }
    return true;
}


function validFund(str) {
    // 非0开头的数（1~4）位
    var myreg = /^([1-9]\d{0,3})$/;
    if(!myreg.test(str)) {
        return false;
    }
    return true;
}


function validAccount(str) {
    // 账号只包含字母和数字，长度在 3-20 之间
    var myreg = /^[a-zA-Z0-9]{3,20}$/;
    if (!myreg.test(str)) {
        return false;
    }
    return true;
}   


function validPassword(str) {
    // 密码只包含字母和数字，长度在 6-20 之间
    var myreg = /^[a-zA-Z0-9]{6,20}$/;
    if (!myreg.test(str)) {
        return false;
    }
    return true;
}


function validName(str) {
    // 姓名只能包含汉字，长度在 2-4 之间
    var myreg = /^[\u4e00-\u9fa5]{2,4}$/;
    if(!myreg.test(str)) {
        return false;
    }
    return true;
}


function showMyAlert(message) {
    if($("#my-alert").hasClass("alert-success")) {
        $("#my-alert").removeClass("alert-success")
    }
    if(!$("#my-alert").hasClass("alert-danger")) {
        $("#my-alert").addClass("alert-danger")
    }
    $("#my-alert")
        .find("strong")
        .text("失败！")
        .end()
        .find("span")
        .text(message)
        .end()
        .show();
}

function showSuccess(message) {
    if($("#my-alert").hasClass("alert-danger")) {
        $("#my-alert").removeClass("alert-danger")
    }
    if(!$("#my-alert").hasClass("alert-success")) {
        $("#my-alert").addClass("alert-success")
    }
    $("#my-alert")
        .find("strong")
        .text("成功！")
        .end()
        .find("span")
        .text(message)
        .end()
        .show();
}


function showSuccessHide(message, mseconds) {
    if($("#my-alert").hasClass("alert-danger")) {
        $("#my-alert").removeClass("alert-danger")
    }
    if(!$("#my-alert").hasClass("alert-success")) {
        $("#my-alert").addClass("alert-success")
    }
    $("#my-alert")
        .find("strong")
        .text("成功！")
        .end()
        .find("span")
        .text(message)
        .end()
        .show()
        .delay(mseconds)
        .hide(0);
}


function hideMyAlert() {
    $("#my-alert").hide(0);
}


function del() {
    var msg = "确定删除吗？";
    if (confirm(msg) === true){
        return true;
    }
    return false;
}