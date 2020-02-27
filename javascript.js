Promises:

function myAsyncFunction(){
	let error = True
	let promise = new Promise(()=>{
		setTimeout((response,reject)=>{
			if (error){
				reject("Error");
			}
			else{
				console.log("changed the log")
				response("Success")
			}
		},1000);
	});
	
	return promise;

}

myAsyncFunction().then(
	(success)=>{console.log(success)},
	(error)=>{console.log(error),

)

