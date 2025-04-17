export function webpSupportTest() {
  let webP = new Image();
  webP.src =
    'data:image/webp;base64,UklGRjoAAABXRUJQVlA4IC4AAACyAgCdASoCAAIALmk0mk0iIiIiIgBoSygABc6WWgAA/veff/0PP8bA//LwYAAA';
  webP.onload = webP.onerror = () => {
    supportTest(webP.height == 2);
  };
}
const testingItem = document.querySelector('html');
const supportTest = (support) => {
  support ? testingItem.classList.add('_webp') : testingItem.classList.add('_no-webp');
};

//Старая версия без модуля
// function webpSupportTest(callback) {
// 	let webP = new Image();
// 	webP.onload = webP.onerror = function () {
// 		callback(webP.height == 2);
// 	};
// 	webP.src = "data:image/webp;base64,UklGRjoAAABXRUJQVlA4IC4AAACyAgCdASoCAAIALmk0mk0iIiIiIgBoSygABc6WWgAA/veff/0PP8bA//LwYAAA";
// }
// webpSupportTest(function (support) {
// 	if (support === true) {
// 		document.querySelector('html').classList.add('_webp');
// 	} else {
// 		document.querySelector('html').classList.add('_no-webp');
// 	}
// });
