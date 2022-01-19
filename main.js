function fazGet(url){
    


let request = new XMLHttpRequest()
request.open("GET", url,false)
//request.withCredentials = true;
request.setRequestHeader("Content-Type", "text/plain;charset=UTF-8");
request.send(null)

return request.responseText
//console.log(request.responseText)


/*
var request = createCORSRequest("GET",url);
request.send();
console.log(request.responseText);
*/
}

function criarlinha(pedido){


}

function main(){


    
   let data = fazGet("http://127.0.0.1:5000/category")
   let pedido = JSON.parse(data);
    console.log(pedido)
}

main()