// $(document).ready(function(){
//
// 	function toTitleCase(str) {
// 	    return str.replace(/(?:^|\s)\w/g, function(match) {
// 	        return match.toUpperCase();
// 	    });
// 	}
//
// 	$("#history_table").dataTable();
// 	$.ajax({
// 		url:'/save_access_page_form_data',
// 		data:{
// 			get_users_acccess_controlling_in_header:1,
// 		},
// 		dataType:'JSON',
// 		method:'get',
// 		success:function(data){
// 			if (data['pages'].length==0){
// 				console.log("Not restriction for this user");
// 			}
// 			else{
// 				$('.appending_lis').remove();
// 				for (var i=0;i<data['pages'].length;i++){
// 					let page = data['pages'][i];
// 					let page_format = page.replaceAll("_"," ").replace("tab","");
// 					let li_element='<li class="appending_lis"><a href="'+page+'" id="'+page+'"  class="waves-effect"><span> '+toTitleCase(page_format)+' </span></a></li>';
// 					$(li_element).insertAfter($("#insert_after"));
// 					// console.log(page);
// 				}
// 			}
// 		}
// 	});  // end ajax call here
//
//
//
//
//
// $(document).on('click','.delete_access',function(){
// 	let row_id = $(this).closest('tr').prop('id');
// 	let writer_id = $(this).attr('data-id');
// 	let page_name = $(this).attr('id');
// 	$.ajax({
// 			url:'/save_access_page_form_data',
// 			method:'get',
// 			data:{
// 					writer_id:writer_id,
// 					page_name:page_name,
// 					delete_page_access:1,
// 				},
// 			dataType:'JSON',
// 			success:function(data){
// 				if (data['flag']==1)
// 					$("#"+row_id).remove();
// 				else
// 					alert("Error in deletion")
// 			}
// 		}); //end ajax
// 	});
//
// $(document).on('submit','#saving_status_form',function(e){
// 	let data = $(this).serialize()+"&save_page_status=1";
// 	let writer_name = $("#writer_id").find(":selected").text();
// 	let page_name = $("#page_name").val();
//  	$.ajax({
// 		url:'/save_access_page_form_data',
// 		method:'get',
// 		data:data,
// 		dataType:'JSON',
// 		success:function(data){
// 			if (data['success']==1)
// 				$("#success").html('The <strong>'+page_name+'</strong> access has been assigned to '+writer_name+' successfully').show();
// 			else if(data['error']==1)
// 				$("#error").html('The <strong>'+page_name+'</strong> is already exists againt '+writer_name+'').show();
// 			setTimeout(function(){ $('.alert').hide(); }, 10000); // 10 second delay
// 			$("#saving_status_form")[0].reset();
// 		}
// 	});
// 	e.preventDefault();
// });
//
// $(document).on('change','#writer_id_see_track_for_accesss',function(){
// 	let writer_name = $("#writer_id_see_track_for_accesss").find(":selected").text();
// 	let writer_id = $("#writer_id_see_track_for_accesss").find(":selected").val();
// 	$.ajax({
// 		url:'/save_access_page_form_data',
// 		dataType:'json',
// 		method:'get',
// 		data:{
// 			get_page_status:1,
// 			writer_name:writer_name,
// 			writer_id:writer_id,
// 		},
// 		success:function(data){
// 			$("#result_appenderr").empty();
// 			if(data['data'].length>0){
// 				for (var i =0; i<data['data'].length;i++){
// 					$("#page_showing").show();
// 					let page_name = data['data'][i].page_name;
// 					let buttons = '<button class="btn btn-md btn-danger delete_access" title="Remove This Page" id="'+page_name+'" data-id="'+writer_id+'"><i class="fa fa-trash"></i></button>';
// 					let tr = '<tr id="tr_row_'+i+'"><td>'+(parseInt(i)+1)+'</td><td>'+page_name+'</td><td>'+buttons+'</td></tr>';
// 					$("#result_appenderr").append(tr);
// 				}
// 			}
// 		}
// 	});  //end ajax here
// });
//
// 	function sleep(ms) {
//   		return new Promise(resolve => setTimeout(resolve, ms));
// 	}
// $(document).on('click','.copy_text',function() {
// 		let href = document.location.href;
// 		let tab_name = href.substr(href.lastIndexOf('/') + 1);
// 		//let whole_para = $("#content_"+);
// 		let para_number = $(this).attr('data-id').replace('content_','paragraph_');
// 		let id = $(this).attr('data-id');
// 		let whole_para_content = $("#"+id).html();
//
// 		$.ajax({
// 			url:'save_writer_activity',
// 			method:'get',
// 			dataType:'JSON',
// 			data:{
// 				'tab_name':tab_name,
// 				'para_number':para_number,
// 				'whole_para_content':whole_para_content,
// 			},
// 			success:function(data){
// 				if (data['success']==1){
// 						$(".content_shower_p").removeClass('highleight');
// 						$(".content_shower_tag").removeClass('highleight');
//
//
// 						$("#"+id).addClass('highleight');
// 						var r = document.createRange();
// 						r.selectNode(document.getElementById(id));
// 						window.getSelection().removeAllRanges();
// 						window.getSelection().addRange(r);
// 						document.execCommand('copy');
// 						window.getSelection().removeAllRanges();
// 						$.Notification.autoHideNotify('black','top center', 'Success!', 'Paragraph Copied!');
// 				}
// 			}
// 		});
// });
// /// used for copying the heading
// $(document).on('click','.copy_heading',function() {
// 		//let para_number = $(this).attr('data-id').replace('content_','paragraph_');
// 		let id = $(this).attr('id').replace("copy_btn_","");
//
// 		let whole_heading = $("#row_"+id).find("td:first").html().split(") ");
// 		$(".text-bold").removeClass('highleight');
// 				$("#row_"+id).find("td:first").addClass('highleight');
// 		var r = document.createRange();
// 		r.selectNode(document.getElementById("row_"+id));
// 		window.getSelection().removeAllRanges();
// 		window.getSelection().addRange(r);
// 		document.execCommand('copy');
// 		window.getSelection().removeAllRanges();
// 		$.Notification.autoHideNotify('black','top center', 'Success!', 'Heading Copied!');
// });
//
// //copy tag only on each tab
// $(document).on('click','.copy_tag',function() {
// 		let tag_data_id = $(this).attr('data-id');
// 		$(".content_shower_tag").removeClass('highleight');
// 		$(".content_shower_p").removeClass('highleight');
// 		$("#"+tag_data_id).addClass('highleight');
// 		var r = document.createRange();
// 		r.selectNode(document.getElementById(tag_data_id));
// 		window.getSelection().removeAllRanges();
// 		window.getSelection().addRange(r);
// 		document.execCommand('copy');
// 		window.getSelection().removeAllRanges();
// 		$.Notification.autoHideNotify('black','top center', 'Success!', 'Tags Copied!');
// });
//
// $(document).on('click','.shhow_paragraph',function(){
// 	let paragraph=$(this).attr('data-id');
// 	let sequence_of_paragraph= $(this).attr('id');
// 	$("#myLargeModalLabel").empty().html(sequence_of_paragraph);
// 	$("#modalData").empty().append(paragraph);
// 	$("#customMODAL").modal('show');
//
// });
//
//
// $(document).on('keypress','#ticker',function (e) {
//  var key = e.which;
//  if(key == 13)  // the enter key code
//   {
//     $('#process_btn').click();
//     return false;
//   }
// });
//
// 		$(document).on('click','#process_btn',function(e){
//
// 			let notification='<div class="alert alert-info text-center"><p>Please Wait..</p></div>';
// 			let href = document.location.href;
// 			let page_name = href.substr(href.lastIndexOf('/') + 1);
// 			let ticker = $("#ticker").val();
// 			const process_building = async _ => {
// 		            console.log('Start');
// 		                await $.ajax({
// 		                    url: 'process_tabs',
// 		                    data:{
// 		                    	'page_name':page_name,
// 		                    	'ticker':ticker,
// 		                    },
// 		                    dataType: 'json',
// 		                    method: 'GET',
// 		                    beforeSend:function(){
// 		                    	for (let i =1 ; i<101;i++)
// 		                    	{
// 		                    		let c=i;
// 		                    		let yy='<div class="progress"><div class="progress-bar progress-bar-purple wow animated progress-animated animated" role="progressbar" aria-valuenow="'+c+'" aria-valuemin="0" aria-valuemax="100" style="width: '+c+'%; visibility: visible; animation-name: animationProgress;"><span class="sr-only">100% Complete</span></div></div>';
// 		                    		$("#form_ticker_div").empty().append(notification+yy);
// 		                    		sleep(3000);
// 		                    	}
// 		                    },
// 		                    success: function(data) {
// 		                    	let total_size_of_paras = data.length;
// 		                    	if (page_name=="headings_tab" || page_name=="penny_stock_headings_tab" || page_name=="general_headings_tab"){
// 		                    			let msg='<div class="alert alert-success text-center"><strong>There are total '+total_size_of_paras+' Headings</strong></div>';
// 			                    	$("#generation_results").empty().append(msg);
// 			                    	let table="<table class='table table-hover'><thead><tr><th>Heading</th><th>Action</th></thead><tbody>";
// 			                    	let table_end = "</tbody></table>";
// 			                    	let rows ="";
// 			                    	for (let i = 0; i<total_size_of_paras;i++){
// 			                    		if (i==0)
// 			                    			$("#form_ticker_div").remove();
// 			                    		let count = i+1;
// 			                    		let heading = data[i];
// 			                    		let btn="<button class='copy_heading btn btn-sm btn-danger' id='copy_btn_"+count+"'><i class='fa fa-file'></i></button>";
// 			                    		rows=rows+"<tr id='row_"+count+"'><td class='text-bold'>"+count+") "+heading+"</td><td>"+btn+"</td></tr>";
// 			                    	}//end for loop here
// 			                    	$("#generation_results").append(table+rows+table_end);
//
// 		                    	}else{
// 			                    	let msg='<div class="alert alert-success text-center"><strong id="total_paras_generated">There are total '+(parseInt(total_size_of_paras)-1)+' paragraphs</strong></div>';
// 			                    	$("#generation_results").empty().append(msg);
// 				                    	for (let i = 0; i<total_size_of_paras;i++){
// 				                    		if (i==0)
// 				                    			$("#form_ticker_div").remove();
// 				                    		let count = i+1;
// 				                    		let para = data[i];
//
// 				                    		let append_div ="<div class= 'panel panel-color panel-inverse'  id='panel_"+count+"'><div class='panel-heading'> <h3 class='panel-title'>Paragraph # "+count+"</h3></div><div class='panel-body' id='paragraph_"+count+"'><p id='content_"+count+"' class='content_shower_p'>"+para+"</p><div class='form-group' style='margin-top: 20px;'><button class='btn btn-primary copy_text'  type='button' data-id='content_"+count+"'>Copy to clipboard</button></div></div></div>";
//
// 				                    		if (i==total_size_of_paras-1){
// 				                    			append_div="<div class= 'panel panel-color panel-danger'><div class='panel-heading'> <h3 class='panel-title'>Tags:</h3></div><div class='panel-body' id='tags'><p id='content_"+count+"' class='content_shower_tag'>"+para+"</p><div class='form-group' style='margin-top: 20px;'><button class='btn btn-primary copy_tag'  type='button' data-id='content_"+count+"'>Copy to clipboard</button></div></div></div>";
// 				                    		}
// 				                    		$("#generation_results").append(append_div);
// 				                    	}//end for loop here
// 			                    	get_writer_status();
// 		                    	}  //enn else here
// 		                    },
// 		                    error: function(xhr) { // if error occured
// 					        		$("#form_ticker_div").empty().append(xhr.statusText + xhr.responseText);
// 					    },
// 		                }); //end ajax
//
// 		        } //end for async
// 		    if (ticker!="")
// 		    	process_building();
// 		    else
// 		    	alert("Enter A Ticker For Generation");
// 		    // e.preventDefault();
// 		}); //end fn..
//
// /////////// update copy status in panels of paragraphs
// function get_writer_status(){
// 	//let total_paras_generated =  parseInt($("#total_paras_generated").text().replace(/[^0-9.]/g, ""));
// 	let href = document.location.href;
// 	let tab_name = href.substr(href.lastIndexOf('/') + 1);
// 	$.ajax({
// 		url:'process_copy_status',
// 		method:'get',
// 		data:{
// 			'tab_name':tab_name,
// 		},
// 		dataType:'json',
// 		success:function(data){
// 			for (let i =0;i<data.length;i++){
//
// 				let paragraph_number_index =data[i].paragraph_number_index;
// 				let copies = data[i].copies;
// 				let date_time_ago  = data[i].date_time_ago;
// 				let writer_name = data[i].writer_name;
// 				let text = "<div class='copied_information'><p class='text-danger' style='font-size: 16px;'><strong>Copies Used: </strong>"+copies+" <strong>Last Used: </strong>"+date_time_ago+" ago <strong>By: </strong>"+writer_name+"</p>";
// 				$("#paragraph_"+paragraph_number_index).append(text);
// 			}
// 		}
// 	});
// }
// }); //end ready fn.. here