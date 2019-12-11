class General{

    constructor(){}

    clearBody() {
        try {
            var div = document.getElementById("body-placeholder");
            div.innerHTML = '';
        } catch (Exception) { }
    }

    makeButton(text) {
        var button = document.createElement("button");
        button.setAttribute("type", "button");
        button.setAttribute("class", "btn btn-secondary waves-effect waves-light");
        button.appendChild(document.createTextNode(text));
        return button;

    }

    async getData(link) {
        try {
            // let response = ;
            let data = await (await fetch(link)).json();
            return data;
        } catch (Exception) {
            console.log(Exception);
            // clearInterval(btime);
        }
    }

    replace_content(html_file, div_id){
        $.get(html_file, function (data) {
            $("#"+div_id).replaceWith(data);
        });
    }

    print(msg){
        console.log(msg);
    }

    putCard(div_id, card_body){
        var div = document.getElementById(div_id);
        var content = `
        <div class="card card-body bg-light">
            <div class="card-body">
                `+card_body +`
            </div>
        </div>
        `;
        div.innerHTML=content
    }
}
