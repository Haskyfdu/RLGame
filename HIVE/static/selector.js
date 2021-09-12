// default value
let SelectedAction = '-- choose --';
let SelectedPiece = '-- choose --';
let SelectedDestination = '-- choose --';
let SelectedPlayer = 'Hasky';
let PostData = {
    'action': SelectedAction,
    'piece': SelectedPiece,
    'destination': SelectedDestination,
    'player': SelectedPlayer};

// first loading
function selector_initialization() {
    let data = ajax_post_to_map_page(PostData);

    let player_option = document.getElementById('player');
        player_option.add(new Option(SelectedPlayer));
        player_option.value = SelectedPlayer;

    let action_option = document.getElementById('action');
        action_option.add(new Option('Place'));
        action_option.add(new Option('Move'));
        action_option.add(new Option('Pass'));
        action_option.value = SelectedAction;

    let piece_option = document.getElementById('piece');
        piece_option.value = SelectedPiece;

    let destination_option = document.getElementById('destination');
        destination_option.value = SelectedDestination;
}

// Action selector
function Action_selector(action) {
    SelectedAction = action;
    if (action === 'Place'){
        $.ajax({
        type: 'POST',
        url: '/ValidPlace',
        data: JSON.stringify(post_data),
        contentType: "application/json;charset=utf-8",
        async: false,
        success: function(recall_data) {
            let city_list = recall_data[''];
            console.log(city_list)
        },
        error: function(recall_error) {
            console.log(recall_error);
            console.log('error on loading city info data');
        }
    });


        let piece_option = document.getElementById('piece');
        piece_option.add(new Option('-- choose --'));
        piece_option.add(new Option('QueenBee'));
        piece_option.add(new Option('Grasshopper'));
        piece_option.add(new Option('Beetle'));
        piece_option.add(new Option('SoldierAnt'));
        piece_option.add(new Option('Spider'));
        piece_option.value = SelectedPiece;
    }
}


function city_selector(city_value) {
    SelectedCity = city_value;
    map.setZoomAndCenter(map.getZoom(), CityList[SelectedProvince][SelectedCity]);
    //List_all = ajax_post_to_map_page(PostData);
    //CityList = List_all['city'];
}

function hex_selector(hex_value) {
    SelectedHex = hex_value;
    map.clearMap();
    plot_hex_list2(List_all['hex'][SelectedHex], CityList[SelectedProvince][SelectedCity]);
}


