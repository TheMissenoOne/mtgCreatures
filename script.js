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
        Object.keys(data).forEach(element => {
          let link = document.createElement("a")
          link.href = '?card=' + data[element].name
          link.appendChild(document.createTextNode(data[element].name))
          document.getElementById("cards").append(link)
        });
        console.log(card)
        document.getElementById("ficha").insertAdjacentHTML('afterbegin', getStatBlock(data[card]))

      });
  } catch (err) {
    console.log("Issues with Parsing URL Parameter's - " + err);
  }
}

const getStatBlock = (data) => '<div class="card_art" style="background-image: url(' + data.image_uris.art_crop + ')"><stat-block>\
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
  <property-line>\
    <h4>Damage Immunities</h4>\
    <p>' + data['Damage Immunities'] + '</p>\
  </property-line>\
  <property-line>\
  <h4>Damage Resistances</h4>\
  <p>' + data['Damage Resistances'] + '</p>\
</property-line>\
  <property-line>\
    <h4>Condition Immunities</h4>\
    <p>' + data['Condition Immunities'] + '</p>\
  </property-line>\
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