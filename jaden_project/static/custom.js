// if (localStorage.getItem("loggedin")) {
//     let check = localStorage.getItem("loggedin");
//     if (check == 0) {
//         location.href = "login";
//     }
// } else {
//     location.href = "login";
// }
// $('#ticker_container').submit(function(e) {
//
//     let form_data = $("#ticker_container").serialize();
//     var format_name_text = $("#formate_selection").find(':selected').text();
//     var format_name = $("#formate_selection").find(':selected').val().trim();
//     $("#para_append").append('<h3 class = "alert alert-success text-center"> ' + format_name_text + ' </h3>');
//     let ticker_box = $("#ticker_box").val().split("\n");
//     let heading_num = $("#heading_name").val();
//
//     //$("#format_name_mapping").empty().append('');
//     const forLoop = async _ => {
//             console.log('Start');
//             for (let i = 0; i < ticker_box.length; i++) {
//                 //let h_index = i;
//                 //let file_num = i + 1;
//
//                 let ticker = ticker_box[i].trim();
//                 // if (heading_num > 0)
//                 //     let h_index = heading_num;
//                 let fn = parseInt(heading_num) + 1;
//                 if (parseInt(heading_num) > 0) {
//                     fn = parseInt(heading_num);
//                 }
//
//                 let counter = i + 1;
//                 $("#progress_div").empty().append('<div class="alert alert-info text-center"><strong>' +
//                     counter + ':' + ticker + ' is Processing.</strong></div>');
//                 await $.ajax({
//                     url: 'validate_username',
//                     data: {
//                         'ticker': ticker,
//                         'h_index': i,
//                         'file_number': fn,
//                         'iteration': i,
//                         'formate_selection': format_name,
//                         // 'form_data': form_data,
//                     },
//                     dataType: 'json',
//                     method: 'get',
//                     success: function(data) {
//                         $("#ticker_container").empty();
//                         $("#para_append").append(data[0]);
//                         //remove progress div when last ticker done
//                         if (i == ticker_box.length - 1) {
//                             $("#progress_div").remove();
//                             $(".navbar-fixed-top").remove();
//                         }
//
//                     }
//                 }); //end ajax
//             } //end for
//         } //end for async
//         // #########################
//     forLoop();
//     e.preventDefault();
// }); //end fn..