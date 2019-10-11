$(function() {
    //var sourceDataObj = jQuery.parseJSON( "https://jsonplaceholder.typicode.com/comments" );
  
    //THIS SMALL SAMPLE WORKS
    var sourceDataObj = [
      { id: "1", value: "red" },
      { id: "2", value: "green" },
      { id: "3", value: "blue" },
      { id: "4", value: "yellow" }
    ];
  
    $("#search").tokenfield({
      autocomplete: {
        source: sourceDataObj,
        delay: 100
      },
      showAutocompleteOnFocus: true
    });
  
    $("#search")
      .on("tokenfield:createtoken", function(event) {
        var existingTokens = $(this).tokenfield("getTokens");
        var exists = true;
        //PREVENT DUPLICATION
        $.each(existingTokens, function(index, token) {
          if (token.value === event.attrs.value) event.preventDefault();
        });
        //ALLOW ONLY TOKENS FROM SOURCE
        $.each(sourceDataObj, function(index, token) {
          if (token.value !== event.attrs.value) exists = false;
        });
        if (exists === true) event.preventDefault();
      })
  
      .on("tokenfield:removedtoken", function(event) {
        alert("Token " + event.attrs.value + " removed!");
      });
  });
  