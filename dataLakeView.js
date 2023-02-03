$(document).ready(function () {

    d3.json("data/datalake_sample.json", function (error, data) {
        var tableData = Object.values(data);
        //create Tabulator on DOM element with id "example-table"
        var table = new Tabulator("#datalake-table", {
            // height:800, // set height of table (in CSS or here), this enables the Virtual DOM and improves render speed dramatically (can be any valid css height value)
            data: tableData, //assign data to table
            layout: "fitColumns",
            pagination: "local", //paginate the data
            paginationSize: 10, //allow 5 rows per page of data
            paginationCounter: "rows", //display count of paginated rows in footer
            columns: [ //Define Table Columns
                {
                    title: "ID",
                    hozAlign: "left",
                    formatter: "number",
                    field: "id",
                    width: 75,
                    headerFilter: true
                },
                {
                    title: "Name",
                    hozAlign: "left",
                    field: "name",
                    headerFilter: true
                },
                {
                    title: "Prepared By",
                    hozAlign: "left",
                    field: "prepared_by",
                    headerFilter: true
                },
                {
                    title: "Created On",
                    hozAlign: "left",
                    field: "created_on",
                    formatter: "datetime",
                    headerFilter: false,
                    formatterParams: {
                        inputFormat: "M-d-yyyy",
                        outputFormat: "MM/dd/yyyy",
                        timezone: "America/Los_Angeles",
                    }
                },
                {
                    title: "Last Updated On",
                    hozAlign: "left",
                    field: "updated_on",
                    formatter: "datetime",
                    headerFilter: false,
                    formatterParams: {
                        inputFormat: "M-d-yyyy",
                        outputFormat: "MM/dd/yyyy",
                        timezone: "America/Los_Angeles",
                    }
                },
                {
                    title: "Quality",
                    hozAlign: "center",
                    field: "quality",
                    formatter: "traffic",
                    width: 85,
                    headerFilter: false,
                    formatterParams: {
                        min: 0,
                        max: 100,
                        color: ["#e74c3c", "#f1c40f", "#2ecc71"],
                    },
                    tooltip: function (e, cell, onRendered) {
                        //cell - cell component

                        //function should return a string for the tooltip of false to hide the tooltip
                        var el = document.createElement("div");
                        el.style.backgroundColor = "#dff9fb";
                        el.innerText = cell.getColumn().getDefinition().title + " - " + cell.getValue(); //return cells "field - value";

                        return el;
                    }
                },
                {
                    title: "Usage",
                    hozAlign: "center",
                    field: "usage",
                    formatter: "traffic",
                    width: 85,
                    headerFilter: false,
                    formatterParams: {
                        min: 0,
                        max: 100,
                        color: ["#e74c3c", "#f1c40f", "#2ecc71"],
                    },
                    tooltip: function (e, cell, onRendered) {
                        //cell - cell component

                        //function should return a string for the tooltip of false to hide the tooltip
                        var el = document.createElement("div");
                        el.style.backgroundColor = "#dff9fb";
                        el.innerText = cell.getColumn().getDefinition().title + " - " + cell.getValue(); //return cells "field - value";
                        
                        return el; 
                    }
                }
            ],
        });

        //trigger an alert message when the row is clicked
        table.on("rowClick", function (e, row) {
            // alert("Row " + row.getData().id + " Clicked!!!!");
            $('.nav-tabs a[href="#' + "nav-dataset" + '"]').tab('show');
        });
    });

});