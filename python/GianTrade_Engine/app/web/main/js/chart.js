class GTchart {
    constructor() { 
        let mChart = document.getElementById('gtchart').getContext('2d');
        let gt = new Chart(mChart, {
            type:'bar',
            data:{
                labels:['1','2','3','4','5'],
                datasets:[{
                    label:"pop",
                    data:[0,1,2,3,4]
                }]
            },
            options:{
                responsive: true,
                // Boolean - whether to maintain the starting aspect ratio or not when responsive, if set to false, will take up entire container
                maintainAspectRatio: true,}
        });
    }
}