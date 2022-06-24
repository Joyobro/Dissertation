var controls = {
    leftArrow: '<i class="fal fa-angle-left" style="font-size: 1.25rem"></i>',
    rightArrow: '<i class="fal fa-angle-right" style="font-size: 1.25rem"></i>'
}

var token = '{{csrf_token}}';

$('#bodpicker').datepicker(
    {
        todayBtn: "linked",
        clearBtn: true,
        todayHighlight: true,
        templates: controls
    });

$('#lookup_field').setupPostcodeLookup({
    api_key: 'ak_k3nfhahuRDdzvuVFwfKzjr5dn64Of',
    output_fields: {
        line_1: '#first_line',
        line_2: '#second_line',
        line_3: '#third_line',
        post_town: '#post_town',
        postcode: '#postcode'
    },
    input: '#postcode_address',
    button: '#findaddressbutton',
    dropdown_class: 'custom-select',
    dropdown_container: '#addressoutput'
});

$("#saveprofile").on("click", () => {
    var today = new Date();
    var date = today.getFullYear() + '-' + (today.getMonth() + 1) + '-' + today.getDate();
    today = new Date();
    dob = new Date($("#bodpicker").val());
    age = new Date(today - dob).getFullYear() - 1970;
    newrow = {
        "name": $("#firstname").val() + " " + $("#lastname").val(),
        "gender": $("#gender option:selected").text(),
        "age": age,
        "contact": $("#contactno").val(),
        "email": $("#email").val(),
        "address": $("#idpc_dropdown option:selected").text(),
        "famcontact": $("#famcontactno").val(),
        "deviceid": $("#deviceselector").val(),
    };

    newrow.orgid = '{{ orgid }}'
    var token = '{{csrf_token}}';
    console.log(newrow);
    // {#$.ajax({#}
    // {#    type: "POST",#}
    // {#    headers: {"X-CSRFToken": token},#}
    // {#    url: "{% url 'service:device' %}",#}
    // {#    data: newrow,#}
    // {#    dataType: 'json',#}
    // {#    success: function (result) {#}
    // {#        if (result.status == "success") {#}
    // {#            var table = $('#devicetable').DataTable();#}
    // {#            table.row.add(newrow).draw()#}
    // {#            $('#devicemodal').modal("hide")#}
    // {#        } else {#}
    // {##}
    // {#        }#}
    // {#    }#}
    //);}
    //  success(rowdata);


})

//define column for the datatable
var columnSet = [
    {
        title: "profileid",
        id: "profileid_id",
        data: "profileid_id",
        placeholderMsg: "Server Generated ID",
        "visible": false,
        "searchable": false,
        type: "readonly"
    },
    {
        title: "Name",
        id: "name",
        data: "name",
        type: "text"
    },
    {
        title: "Gender",
        id: "gender",
        data: "gender",
        type: "text"
    },
    {
        title: "Age",
        id: "age",
        data: "age",
        type: "text"
    },
    {
        title: "Contact",
        id: "contactno",
        data: "contactno",
        type: "text"
    },
    {
        title: "Email",
        id: "email",
        data: "email",
        type: "text",
    },
    {
        title: "Home Address",
        id: "address",
        data: "address",
        type: "text",
    },
    {
        title: "Family Contact",
        id: "famcontact",
        data: "famcontact",
        type: "text",
    },
    {
        title: "Assigned Device",
        id: "deviceid",
        data: "deviceid",
        type: "text",
    }
]

var myTable = $('#dt-basic-example').dataTable(
    {
        /* check datatable buttons page for more info on how this DOM structure works */
        dom: "<'row mb-3'<'col-sm-12 col-md-6 d-flex align-items-center justify-content-start'f><'col-sm-12 col-md-6 d-flex align-items-center justify-content-end'B>>" +
            "<'row'<'col-sm-12'tr>>" +
            "<'row'<'col-sm-12 col-md-5'i><'col-sm-12 col-md-7'p>>",
        // {#ajax: "{% static 'media/data/server-demo.json'  %}",#}
        columns: columnSet,
        lengthMenu: [10, 20, 50, 100],
        lengthChange: true,
        /* selecting multiple rows will not work */
        select: 'single',
        /* altEditor at work */
        altEditor: false,
        responsive: true,
        /* buttons uses classes from bootstrap, see buttons page for more details */
        buttons: [
            {
                extend: 'selected',
                text: '<i class="fal fa-times mr-1"></i> Delete',
                name: 'delete',
                className: 'btn-primary btn-sm mr-1'
            },
            {
                extend: 'selected',
                text: '<i class="fal fa-edit mr-1"></i> Edit',
                name: 'edit',
                className: 'btn-primary btn-sm mr-1'
            },
            {
                text: '<i class="fal fa-plus mr-1"></i> Add',
                name: 'add',
                className: 'btn-success btn-sm mr-1',
                action: function (e, dt, node, config) {
                    $.ajax({
                        "headers": {"X-CSRFToken": token},
                        "url": "{% url 'service:device' %}?orgid={{ orgid }}",
                        "type": "GET",
                        success: function (result) {
                            console.log(result)
                            // for (let device of result.data) {
                            //     if (device.status == "Available") {
                            //         $('#deviceselector').append($('<option></option>').val(device.id).html(device.id));
                            //     }
                            // }
                        }
                    });
                    $("#profilemodal").modal();
                }
            },
            {
                text: '<i class="fal fa-sync mr-1"></i> Refresh',
                name: 'refresh',
                className: 'btn-primary btn-sm'
            }],
        columnDefs: [
            {
                targets: 1,
                render: function (data, type, full, meta) {
                    var badge = {
                        "active":
                            {
                                'title': 'Active',
                                'class': 'badge-success'
                            },
                        "inactive":
                            {
                                'title': 'Inactive',
                                'class': 'badge-warning'
                            },
                        "disabled":
                            {
                                'title': 'Disabled',
                                'class': 'badge-danger'
                            },
                        "partial":
                            {
                                'title': 'Partial',
                                'class': 'bg-danger-100 text-white'
                            }
                    };
                    if (typeof badge[data] === 'undefined') {
                        return data;
                    }
                    return '<span class="badge ' + badge[data].class + ' badge-pill">' + badge[data].title + '</span>';
                },
            },
            {
                targets: 7,
                type: 'currency',
                render: function (data, type, full, meta) {
                    //var number = Number(data.replace(/[^0-9.-]+/g,""));
                    if (data >= 0) {
                        return '<span class="text-success fw-500">$' + data + '</span>';
                    } else {
                        return '<span class="text-danger fw-500">$' + data + '</span>';
                    }
                },
            },
            {
                targets: 6,
                render: function (data, type, full, meta) {
                    var package = {
                        "free":
                            {
                                'title': 'Free',
                                'class': 'bg-fusion-50',
                                'info': 'Free users are restricted to 30 days of use'
                            },
                        "silver":
                            {
                                'title': 'Silver',
                                'class': 'bg-fusion-50 bg-fusion-gradient'
                            },
                        "gold":
                            {
                                'title': 'Gold',
                                'class': 'bg-warning-500 bg-warning-gradient'
                            },
                        "platinum":
                            {
                                'title': 'Platinum',
                                'class': 'bg-trans-gradient'
                            },
                        "payg":
                            {
                                'title': 'PAYG',
                                'class': 'bg-success-500 bg-success-gradient'
                            }
                    };
                    if (typeof package[data] === 'undefined') {
                        return data;
                    }
                    return '<div class="has-popover d-flex align-items-center"><span class="d-inline-block rounded-circle mr-2 ' + package[data].class + '" style="width:15px; height:15px;"></span><span>' + package[data].title + '</span></div>';
                },
            },],

        /* default callback for insertion: mock webservice, always success */
        onAddRow: function (dt, rowdata, success, error) {
            console.log("Missing AJAX configuration for INSERT");
            success(rowdata);


        },
        onEditRow: function (dt, rowdata, success, error) {
            console.log("Missing AJAX configuration for UPDATE");
            success(rowdata);

        },
        onDeleteRow: function (dt, rowdata, success, error) {
            console.log("Missing AJAX configuration for DELETE");
            success(rowdata);

        },
    });
