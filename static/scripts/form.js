$('#generate-button').click(function(event) {
    // Prevent redirection with AJAX for contact form
    var form = $('#synthetic-form');
    var form_id = 'synthetic-form';
    var url = "/generatemaster";
    var type = form.prop('method');
    var stores = getstores()
    var synthetic_generator = getSyntheticcheked()
    console.log(synthetic_generator)
    var output = getoutput_params();
    console.log(output)
    var formData = getFormData(form_id);
    formData.append("synthetic_generator", synthetic_generator);
    formData.append("stores", stores);
    formData.append("output_params", output);
    event.preventDefault();

    if (validtate_output(formData, output)) {
        // submit form via AJAX
        send_form(form, form_id, url, type, modular_ajax, formData);
    }

});

$('#download-button').click(function(event) {

    console.log("download button click")
        // Prevent redirection with AJAX for contact form
    var form = $('#synthetic-form');
    var form_id = 'synthetic-form';
    var url = "/downloadcsv";
    var type = form.prop('method');
    var stores = getstores()
    var synthetic_generator = getSyntheticcheked()
    console.log(synthetic_generator)
    var output = getoutput_params();
    console.log(output)
    var formData = getFormData(form_id);
    formData.append("synthetic_generator", synthetic_generator);
    formData.append("stores", stores);
    formData.append("output_params", output);

    if (validtate_output(formData, output)) {
        // submit form via AJAX
        send_form(form, form_id, url, type, download_ajax, formData);
    }

});
const saveData = (function() {
    const a = document.createElement("a");
    document.body.appendChild(a);
    a.style = "display: none";
    return function(data, fileName) {
        const blob = new Blob([data], { type: "octet/stream" }),
            url = window.URL.createObjectURL(blob);
        a.href = url;
        a.download = fileName;
        a.click();
        window.URL.revokeObjectURL(url);
    };
}());

function get_rights() {
    $.ajax({
        url: '/userrights',
        dataType: "json",
        contentType: "application/json",
        success: function(res) {
            // Success callback
            rights = JSON.parse(res.rights)
            console.log(rights.extract)
            if (rights.generate == false) {
                $("#ext").attr('checked', true);
                $("#gen").attr('checked', false);
                $("#generate").hide()
                $(".fields").hide();
            }
            if (rights.extract == false) {
                $("#gen").attr('checked', true);
                $("#ext").attr('checked', false);
                $("#extract").hide()
            }
        },
        error: function() {
            //any error to be handled
        }
    });
}

function validtate_output(formdata, output) {
    var synchecked = getSyntheticcheked()
    if (synchecked == "New Data Generation") {
        if (output != "") {
            for (var [key, value] of formdata.entries()) {

                if (key == 'customer' && output.indexOf("customer") !== -1) {
                    console.log("customer exist")
                    if (value == '' && value == 0) {
                        M.toast({ html: "Please enter Number of Customer", classes: 'bg-danger text-white',displayLength:3600000  });
                        return false;
                    }
                } else if (key == 'order' && output.indexOf("order") !== -1) {
                    if (value == '' && value == 0) {
                        M.toast({ html: "Please enter Number of Order", classes: 'bg-danger text-white' ,displayLength:3600000 });
                        return false;
                    }
                } else if (key == 'transaction' && output.indexOf("transaction") !== -1) {
                    if (value == '' && value == 0) {
                        M.toast({ html: "Please enter Number of Transaction", classes: 'bg-danger text-white' ,displayLength:3600000 });
                        return false;
                    }
                } else if (key == 'fulfillment' && output.indexOf("fulfillment") !== -1) {
                    if (value == '' && value == 0) {
                        M.toast({ html: "Please enter Number of Fulfillment", classes: 'bg-danger text-white',displayLength:3600000  });
                        return false;
                    }
                }
            }
        } else {
            M.toast({ html: "Please select any Output Parameter", classes: 'bg-danger text-white',displayLength:3600000  });
            return false
        }
    }

    return true
}

function getSyntheticcheked() {
    var selectedVal = $("input[name='data_generator']:checked").val();
    return selectedVal
}

function getstores() {
    stores = []
    $('input[name="store"]:checked').each(function() {
        console.log(this.value);
        stores.push(this.value)
    });

    return stores
}

function getoutput_params() {
    output = []
    $('input[name="output"]:checked').each(function() {
        console.log(this.value);
        output.push(this.value)
    });

    return output
}




function exportCSVFile(items, fileTitle) {

    const replacer = (key, value) => value === null ? '' : value; // specify how you want to handle null values here
    const header = Object.keys(items[0]);
    let csv = items.map(row => header.map(fieldName => JSON.stringify(row[fieldName], replacer)).join(','));
    csv.unshift(header.join(','));
    csv = csv.join('\r\n');
    var exportedFilenmae = fileTitle + '.csv' || 'export.csv';

    var blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    if (navigator.msSaveBlob) { // IE 10+
        navigator.msSaveBlob(blob, exportedFilenmae);
    } else {
        var link = document.createElement("a");
        if (link.download !== undefined) { // feature detection
            // Browsers that support HTML5 download attribute
            var url = URL.createObjectURL(blob);
            link.setAttribute("href", url);
            link.setAttribute("download", exportedFilenmae);
            link.style.visibility = 'hidden';
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }
    }
}

function getFormData(form) {
    // creates a FormData object and adds chips text
    var formData = new FormData(document.getElementById(form));
    //    for (var [key, value] of formData.entries()) { console.log('formData', key, value);}
    return formData
}

function send_form(form, form_id, url, type, inner_ajax, formData) {
    // form validation and sending of form items

    if (form[0].checkValidity() && isFormDataEmpty(formData) == false) { // checks if form is empty
        event.preventDefault();

        // inner AJAX call
        inner_ajax(url, type, formData);

    } else {
        // first, scan the page for labels, and assign a reference to the label from the actual form element:
        var labels = document.getElementsByTagName('LABEL');
        for (var i = 0; i < labels.length; i++) {
            if (labels[i].htmlFor != '') {
                var elem = document.getElementById(labels[i].htmlFor);
                if (elem)
                    elem.label = labels[i];
            }
        }

        // then find all invalid input elements (form fields)
        var Form = document.getElementById(form_id);
        var invalidList = Form.querySelectorAll(':invalid');

        if (typeof invalidList !== 'undefined' && invalidList.length > 0) {
            // errors were found in the form (required fields not filled out)

            // for each invalid input element (form field) return error
            for (var item of invalidList) {
                M.toast({ html: "Please fill the " + item.label.innerHTML + "", classes: 'bg-danger text-white' ,displayLength:3600000});
            }
        } else {
            M.toast({ html: "Another error occured, please try again.", classes: 'bg-danger text-white',displayLength:3600000 });
        }
    }
}


function isFormDataEmpty(formData) {
    // checks for all values in formData object if they are empty
    for (var [key, value] of formData.entries()) {
        if (key != 'csrf_token') {
            if (value != '' && value != []) {
                return false;
            }
        }
    }
    return true;
}

function download_ajax(url, type, formData) {
    // Most simple modular AJAX building block
    $.ajax({
        url: url,
        type: type,
        data: formData,
        processData: false,
        contentType: false,
        beforeSend: function() {
            // show the preloader (loader bar)
            $('.loader').show()
        },
        complete: function() {
            // hide the preloader (loader bar)
            $('.loader').hide()
        },
        success: function(data) {
            if (!$.trim(data.feedback)) { // response from Flask is empty

                for (var i = 0; i < data.length; i++) {
                    Object.keys(data[i]).forEach(key => {
                        console.log(key)
                        exportCSVFile(data[i][key], key)
                    })

                }


                toast_error_msg = "CSV downloaded successfully";
                toast_category = "success";



            } else { // response from Flask contains elements
                toast_error_msg = data.feedback;
                toast_category = "success";
            }
            // toast_error_msg = JSON.stringify(data);
            // toast_category = "success";

        },
        error: function(xhr, textStatus, errorThrown) {
            console.log(errorThrown)
            console.log("error. see details below.");
            console.log(xhr.status + ": " + xhr.responseText);
            toast_error_msg = errorThrown;
            toast_category = "danger";
            M.toast({ html: toast_error_msg, classes: 'bg-' + toast_category + ' text-white' ,displayLength:3600000 });

        },
    }).done(function() {

        M.toast({ html: toast_error_msg, classes: 'bg-' + toast_category + ' text-white' ,displayLength:3600000 });
    });
};

function modular_ajax(url, type, formData) {
    // Most simple modular AJAX building block
    $.ajax({
        url: url,
        type: type,
        data: formData,
        processData: false,
        contentType: false,
        beforeSend: function() {
            // show the preloader (loader bar)
            $('.loader').show()
        },
        complete: function() {
            // hide the preloader (loader bar)
            $('.loader').hide()
        },
        success: function(data) {
            if (!$.trim(data.feedback)) { // response from Flask is empty

                toast_error_msg = data;
                toast_category = "danger";

            } else { // response from Flask contains elements
                toast_error_msg = data.feedback;
                toast_category = "success";
            }
            // toast_error_msg = JSON.stringify(data);
            // toast_category = "success";

        },
        error: function(xhr, textStatus, errorThrown) {
            console.log(errorThrown)
            console.log("error. see details below.");
            console.log(xhr.status + ": " + xhr.responseText);
            toast_error_msg = errorThrown;
            toast_category = "danger";
        },
    }).done(function() {

        M.toast({ html: toast_error_msg, classes: 'bg-' + toast_category + ' text-white' ,displayLength:3600000 });
    });
};

var csrf_token = "{{ csrf_token() }}";


$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrf_token);
        }
    }
});


function show_error(error){
 console.log(error)
}
// on page load
$(document).ready(function() {
    get_rights();
    $('.loader').hide()
    $('.fixed-action-btn').floatingActionButton();
    $('select').formSelect();
    $("#download-button").hide()
    $('#product').hide();
    $('input:radio[name="data_generator"]').change(
        function() {
            if ($(this).is(':checked') && $(this).val() == 'Download Data Extract') {
                $(".fields").hide();
                $('#product').show();
                $("#generate-button").hide()
                $("#download-button").show()

            }
            if ($(this).is(':checked') && $(this).val() == 'New Data Generation') {
                $(".fields").show();
                $('#product').hide();
                $("#download-button").hide()
                $("#generate-button").show()
            }
        });
});