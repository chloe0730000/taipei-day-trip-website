
let request = new XMLHttpRequest();
// handle cross original resource sharing 
request.open('GET', 'http://3.128.124.38:3000/api/attractions', true);



request.onload = function() {
    if (this.status >= 200 && this.status < 400) {
      let res = request.responseText;
      // alert(res)
      alert(res)
      console.log(res.data);
      console.log(res["data"]);
      // console.log(data.data)
      // data = data["data"];
      // console.log(data);




      /*
      let data = JSON.parse(this.response);
      console.log(data);
      data = data["data"];
      console.log(data);

      
      
      let tbl = document.querySelector("table");
  
      // create table with 3*4 format
      for (let i=0; i<3; i++){
        let row = document.createElement("tr");
        for (let j=0; j<4; j++){
          let cell = document.createElement("td");
  
          // image
          let image = document.createElement("img");
          image.src = data[4*i+j].images.split(",")[0]
          image.className = "img-size";
  
          // image title
          let title = document.createElement("div");
          title.className = "img-title";
          let cellText = document.createTextNode(data[4*i+j].name);
          title.appendChild(cellText);
  
          cell.appendChild(image);
          cell.appendChild(title);
          row.appendChild(cell);
        }
        tbl.appendChild(row);
      }
      
    */

    } 
  };
  
  request.send();