function filterF() {
	var input, filter, ul, li, a, i;
	input = document.getElementById('myFood');
	filter = input.value.toUpperCase();
	div = document.getElementById('myDropdownF');
	a = div.getElementsByTagName('a');
	for (i = 0; i < a.length; i++) {
		if (a[i].innerHTML.toUpperCase().indexOf(filter) > -1) {
			a[i].style.display = '';
		} else {
			a[i].style.display = 'none';
		}
	}
}

function filterE() {
	var input, filter, ul, li, a, i;
	input = document.getElementById('myExercise');
	filter = input.value.toUpperCase();
	div = document.getElementById('myDropdown');
	a = div.getElementsByTagName('a');
	for (i = 0; i < a.length; i++) {
		if (a[i].innerHTML.toUpperCase().indexOf(filter) > -1) {
			a[i].style.display = '';
		} else {
			a[i].style.display = 'none';
		}
	}
}

function filterFood(name) {
	var input = document.getElementById('myFood');
	input.value = name;
	filterF();
}

function filterExercise(name) {
	var input = document.getElementById('myExercise');
	input.value = name;
	filterE();
}
