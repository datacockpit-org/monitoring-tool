$(document).ready(function(){
        
    // Load Dataset-level Efficacy Metrics
    d3.json('data/dataset_insights.json', function (error, dataset) {
        $("#datasetName").text(dataset["name"]);
        $("#datasetSchema").text(dataset["schema"]);
        $("#datasetDescription").text(dataset["description"]);
        $("#datasetColumnCount").text(dataset["stats"]["columns"]);
        $("#datasetRowCount").text(dataset["stats"]["rows"]);
        $("#noBatches").text(dataset["stats"]["no_batches"]);
        $("#datasetPreparer").text(dataset["stats"]["prepared_by"]);
        $("#datasetCreatedOn").text(dataset["stats"]["created_on"]);
        $("#datasetUpdatedOn").text(dataset["stats"]["updated_on"]);

        // "business_implication_insights" is third category, commented.
        var insights = ["quality_insights", "usage_insights"];
        insights.forEach(function(insight){
            Object.keys(dataset["efficacy_insights"][insight]).forEach(function(metric){
                var metricDiv = `<div style='margin-top: 16px;'>
                            <h6>
                                <span>
                                    <i class="fas fa-circle text-${getEfficacyClass(insight, metric, dataset["efficacy_insights"][insight][metric]["value"])}"></i>
                                </span>&nbsp;${dataset["efficacy_insights"][insight][metric]["name"]}&nbsp;(${dataset["efficacy_insights"][insight][metric]["value"]}<span>${dataset["efficacy_insights"][insight][metric]["unit"]}</span>)
                            </h6>
                        </div>`
                $("#" + insight).append(metricDiv);
            });
        });
        
    });

    // Load Dataset Preview
    $('#preview').CSVToTable('data/dataset_sample.csv', {
        startLine: 0
    });    
});