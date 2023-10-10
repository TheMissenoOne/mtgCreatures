window.onload = function () {
  try {
    const url_string = (window.location.href);
    const url = new URL(url_string);
    const card = url.searchParams.get("card");
    fetch("./final.json")
      .then((res) => {
        return res.json();

      })
      .then((data) => {
        document.getElementById('dropdownbtn').addEventListener('click',myFunction)
        Object.keys(data).forEach(element => {
          let link = document.createElement("a")
          link.href = '?card=' + data[element].name
          link.appendChild(document.createTextNode(data[element].name))
          document.getElementById("cards").append(link)
        });
        console.log(card)
        document.getElementById("ficha").insertAdjacentHTML('afterbegin', getStatBlock(data[card]))
        console.log(window.innerHeight)
        console.log(getStatBlock(data[card]).length)
        if(getStatBlock(data[card]).length >= window.innerHeight * 2.6  ){
          document.getElementById('stat-block').setAttribute('data-two-column','')
          document.getElementById('stat-block').style='--data-content-height: calc(100% - 34px);'
        }else{
          document.getElementById('stat-block').removeAttribute('data-two-column')
          document.getElementById('stat-block').style=''
        }

      });
  } catch (err) {
    console.log("Issues with Parsing URL Parameter's - " + err);
  }
}

const getStatBlock = (data) => '<div class="card_art" style="background-image: url(' + data.image_uris.art_crop + ')"><stat-block id="stat-block"> \
<creature-heading>\
  <h1>' + data.name + '</h1>\
  <h2>' + data.meta + '</h2>\
</creature-heading>\
\
<top-stats>\
  <property-line>\
    <h4>Armor Class</h4>\
    <p>' + data['Armor Class'] + '</p>\
  </property-line>\
  <property-line>\
    <h4>Hit Points</h4>\
    <p>' + data['Hit Points'] + '</p>\
  </property-line>\
  <property-line>\
    <h4>Speed</h4>\
    <p>' + data['Speed'] + '</p>\
  </property-line>\
\
  <abilities-block data-str="' + data.STR + '"\
                   data-dex="' + data.DEX + '"\
                   data-con="' + data.CON + '"\
                   data-int="' + data.INT + '"\
                   data-wis="' + data.WIS + '"\
                   data-cha="' + data.CHA + '"></abilities-block>\
\
  ' + immunities(data) + '\
  <property-line>\
    <h4>Senses</h4>\
    <p>' + data.Senses + '</p>\
  </property-line>\
  <property-line>\
    <h4>Languages</h4>\
    <p>' + data.Languages + '</p>\
  </property-line>\
  <property-line>\
    <h4>Challenge</h4>\
    <p>' + data.Challenge + '</p>\
  </property-line>\
</top-stats>\
\
' + data.Traits + '\
<h3>Actions</h3>\
\
' + data.Actions + '\
</stat-block></div>'


const immunities = (data) => {
  let propertyBlocks = data['Damage Immunities'] ?
    '<property-line>\
      <h4>Damage Immunities</h4>\
      <p>' + data['Damage Immunities'] + '</p>\
    </property-line>' : ''
  propertyBlocks = data['Damage Resistances'] ?
  '<property-line>\
    <h4>Damage Resistances</h4>\
    <p>' + data['Damage Resistances'] + '</p>\
  </property-line>':''
  propertyBlocks = data['Condition Immunities'] ?
  '<property-line>\
    <h4>Condition Immunities</h4>\
    <p>' + data['Condition Immunities'] + '</p>\
  </property-line>':''
  return propertyBlocks
}

function myFunction() {
  document.getElementById("cards").classList.toggle("show");
}

function filterFunction() {
  var input, filter, ul, li, a, i;
  input = document.getElementById("myInput");
  filter = input.value.toUpperCase();
  div = document.getElementById("cards");
  a = div.getElementsByTagName("a");
  for (i = 0; i < a.length; i++) {
    txtValue = a[i].textContent || a[i].innerText;
    if (txtValue.toUpperCase().indexOf(filter) > -1) {
      a[i].style.display = "";
    } else {
      a[i].style.display = "none";
    }
  }
}