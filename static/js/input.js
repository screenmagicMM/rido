(function(){
$.validator.setDefaults({
    highlight: function(element) {
        $(element).closest('.form-group').addClass('has-error');
    },
    unhighlight: function(element) {
        $(element).closest('.form-group').removeClass('has-error');
    },
    errorElement: 'span',
    errorClass: 'help-block',
    errorPlacement: function(error, element) {
        if(element.parent('.input-group').length) {
            error.insertAfter(element.parent());
        } else {
            error.insertAfter(element);
        }
    }
});
   $("#ipform").validate({
      rules: { 
      'total_investment': "required",
      'no_of_days' :  "required",
      'areas_no':  "required",
      'no_of_kms':  "required", 
      'petrol_price' : "required",
      'disel_price' : "required",
      'lpg_price' : "required",
      'no_of_drivers' : "required",
      'drive_time_per_drver' : "required",
      'driver_salary' : "required",
      'lpg_cars_no' : "required",
      'petrol_cars_no' : "required",
      'disel_cars_no' : "required",
      'avg_maint_cost' : "required",
      'avg_petrol_maint' : "required",
      'avg_disel_maint' : "required",
      'avg_lpg_maint' : "required"
        
      },
      messages: {
      'total_investment':"Please Enter Total Amount of Investment",
      'no_of_days' :  "Please Enter No of Days you want to Run Simulation",
      'areas_no':  "Please enter No of Areas covered",
      'no_of_kms':  "Please Enter Avg Km per Area", 
      'petrol_price' : "Please enter Petrol Price",
      'disel_price' : "Please enter Disel Price",
      'lpg_price' : "Please enter LPG Price per Cylinder",
      'no_of_drivers' : "Please enter No of Drivers we want to have",
      'drive_time_per_drver' : "Please enter Driving Time per Driver",
      'driver_salary': "Please enter Driver salary per hour per day",
      'lpg_cars_no' : "Please Enter no of LPG Cars we have",
      'petrol_cars_no' : "Please enter no of Petrol Cars we have",
      'disel_cars_no' : "Please enter no of Disel cars we have",
      'avg_maint_cost' : "Please enter Average Maintenance Cost per driver",
      'avg_petrol_maint' : "Please enter Average Maintenace Cost of Petrol Car ",
      'avg_disel_maint' : "Please enter Average Maintenace Cost of  Diesel Car",
      'avg_lpg_maint' : "Please enter Average Maintenace Cost of  LPG Cylinder Car"
        
      },
       /*highlight: function(element) {
        $(element).closest('.form-group').addClass('has-error');
      },
      unhighlight: function(element) {
        $(element).closest('.form-group').removeClass('has-error');
      }*/
     submitHandler: function(form) {
        processForm();
    }
    });
  
  function processForm() {
   event.preventDefault();
   //$("#ipform").valid();
    
    //Investment params
    var total_investment = $("#totinvest").val();
    var no_of_days = $("#noofdays").val();
    //Area Parameter
    var areas_no = $("#noofareas").val();
    var no_of_kms = $("#noofkms").val();
    //Fuel Cost
    var petrol_price = $("#petrolprice").val();
    var disel_price = $("#diselprice").val();
    var lpg_price = $("#lpgprice").val();
    //Driver Cost
    var no_of_drivers = $("#noofdrivers").val();
    var drive_time_per_drver = $("#drvtimeperdrver").val();
    var driver_salary = $("#drvsal").val();
    // No of Cars
    var lpg_cars_no = $("#nooflpgcar").val();
    var petrol_cars_no = $("#noofpetrolcar").val();
    var disel_cars_no = $("#noofdiselcar").val();
    // Maint cost
    var avg_maint_cost = $("#avgmaint").val();
    var avg_petrol_maint = $("#avgpetrolmaint").val();
    var avg_disel_maint = $("#avgdiselmaint").val();
    var avg_lpg_maint = $("#avglpgmaint").val();

    if(total_investment && no_of_days && areas_no && no_of_kms &&
       petrol_price && disel_price && lpg_price && no_of_drivers &&
       drive_time_per_drver && driver_salary && lpg_cars_no && petrol_cars_no &&
       disel_cars_no && avg_maint_cost && avg_petrol_maint && avg_disel_maint &&
       avg_lpg_maint)
    {
      var formdata = {
        'total_investment':total_investment,
        'no_of_days' :  no_of_days,
      //Area Parameter
      'areas_no':  areas_no,
      'no_of_kms':  no_of_kms, 
      //Fuel Cost
      'petrol_price' : petrol_price,
      'disel_price' : disel_price,
      'lpg_price' : lpg_price,
      //Driver Cost
      'no_of_drivers' : no_of_drivers,
      'drive_time_per_drver' : drive_time_per_drver,
      'driver_salary': driver_salary,
      // No of Cars
      'lpg_cars_no' : lpg_cars_no,
      'petrol_cars_no' : petrol_cars_no,
      'disel_cars_no' : disel_cars_no,
      // Maint cost
      'avg_maint_cost' : avg_maint_cost,
      'avg_petrol_maint' : avg_petrol_maint,
      'avg_disel_maint' : avg_disel_maint,
      'avg_lpg_maint' : avg_lpg_maint,
    };
        $.ajax({
        type: "POST",
        url: "simulation", //process to mail
        data: formdata,
        success: function(msg){
            if(msg.Status==="success"){
              alert("Simulation Started ");
            } else if(msg.Status==="exception") {
              alert('Exception in Processing Tasks');
            } else if(msg.Status === "reject") {
              alert('Previous Task not Completed Just Wait SomeTime');
            }
        },
        error: function(){
            alert("failure");
        }
      });
    } else {
      alert('Values are Not Valid');
    }
  

  }
}());
