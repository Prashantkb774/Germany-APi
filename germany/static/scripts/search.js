// getting all required elements
const searchInput = document.querySelector(".searchInput");
const input = searchInput.querySelector("input");
const resultBox = searchInput.querySelector(".resultBox");
const icon = searchInput.querySelector(".icon");
const searchResult = document.querySelector(".search-result");
let linkTag = searchInput.querySelector("a");
let webLink;

searchResult.classList.add("table-hide");

// if user press any key and release
input.onkeyup = (e)=>{
    let userData = e.target.value; //user enetered data
    let emptyArray = [];
    if(userData && userData.length > 2) {
        fetch(window.location.href + '/search/' + userData, {method: 'GET'})
          .then(Result => Result.json())
          .then(data => {
            // Empty the search box.
            resultBox.innerHTML = '';

            // Collect all the Items for the Searched Term.
            emptyArray = data.items.map((item) => {
                // passing return data inside li tag
                return item = '<li key="' + item.key + '" system="' + item.system + '" version_number="' + item.version_number + '" data-access_status="' + item.access_status + '" status_level="' + item.status_level + '"  process_control="' + item.process_control + '" >'+ item.key +' - ' + item.system + '</li>';
            });

            if (emptyArray.length > 0) {
                searchInput.classList.add("active"); //show autocomplete box
                showSuggestions(emptyArray);
                let allList = resultBox.querySelectorAll("li");
                for (let i = 0; i < allList.length; i++) {
                    //adding onclick attribute in all li tag
                    allList[i].setAttribute("onclick", "select(this)");
                }
            }
        }).catch(err => { console.log(err); });
    } else {
        searchInput.classList.remove("active"); //hide autocomplete box
    }
}

function select(selected) {
    searchInput.classList.remove("active"); //hide autocomplete box
    searchResult.classList.remove("table-hide");

    var tbody = document.querySelector("#search-table>tbody");
    for (var i = 0; i < tbody.rows.length; i++) {
        tbody.deleteRow(i);
    }

    var newRow = tbody.insertRow();
    newRow.insertCell().append(selected.getAttribute('key'));
    newRow.insertCell().append(selected.getAttribute('system').toUpperCase());

    newRow.insertCell().append(
      selected.getAttribute('version_number') === null ? 'NA': selected.getAttribute('version_number').toUpperCase());
    newRow.insertCell().append(
      selected.getAttribute('access_status') === null ? 'NA': selected.getAttribute('access_status').toUpperCase());
    newRow.insertCell().append(
      selected.getAttribute('status_level') === null ? 'NA': selected.getAttribute('status_level').toUpperCase());
    newRow.insertCell().append(
      selected.getAttribute('process_control') === null ? 'NA': selected.getAttribute('process_control').toUpperCase());
}

function showSuggestions(list) {
    let listData;
    if(!list.length) {
        userValue = inputBox.value;
        listData = '<li>'+ userValue +'</li>';
    } else {
        listData = list.join('');
    }
    resultBox.innerHTML = listData;
}
