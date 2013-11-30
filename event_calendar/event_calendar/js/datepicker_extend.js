$.extend($.fn.datepicker.defaults, {
    onRender: function(date) {
        if(date.getDay() == 6 || date.getDay() == 0) {
            return 'holiday';
        }
        if(date.getMonth()+1 == 1 && date.getDate() == 1) {
            return 'holiday';
        }
        if(date.getMonth()+1 == 1 && date.getDate() == 6) {
            return 'holiday';
        }
        if(date.getMonth()+1 == 5 && date.getDate() == 1) {
            return 'holiday';
        }
        if(date.getMonth()+1 == 5 && date.getDate() == 3) {
            return 'holiday';
        }
        if(date.getMonth()+1 == 5 && date.getDate() == 19) {
            return 'holiday';
        }
        if(date.getMonth()+1 == 8 && date.getDate() == 15) {
            return 'holiday';
        }
        if(date.getMonth()+1 == 11 && date.getDate() == 1) {
            return 'holiday';
        }
        if(date.getMonth()+1 == 11 && date.getDate() == 11) {
            return 'holiday';
        }
        if(date.getMonth()+1 == 12 && date.getDate() == 25) {
            return 'holiday';
        }
        if(date.getMonth()+1 == 12 && date.getDate() == 26) {
            return 'holiday';
        }
        // begin: dates for easter monday
        // 2013
        if(date.getFullYear() == 2013 && date.getMonth()+1 == 4 && date.getDate() == 1) {
            return 'holiday';
        }
        // 2014
        if(date.getFullYear() == 2014 && date.getMonth()+1 == 4 && date.getDate() == 21) {
            return 'holiday';
        }
        // 2015
        if(date.getFullYear() == 2015 && date.getMonth()+1 == 4 && date.getDate() == 6) {
            return 'holiday';
        }
        // 2016
        if(date.getFullYear() == 2016 && date.getMonth()+1 == 3 && date.getDate() == 28) {
            return 'holiday';
        }
        // 2017
        if(date.getFullYear() == 2017 && date.getMonth()+1 == 4 && date.getDate() == 17) {
            return 'holiday';
        }
        // 2018
        if(date.getFullYear() == 2018 && date.getMonth()+1 == 4 && date.getDate() == 2) {
            return 'holiday';
        }
        // 2019
        if(date.getFullYear() == 2019 && date.getMonth()+1 == 4 && date.getDate() == 22) {
            return 'holiday';
        }
        // 2020
        if(date.getFullYear() == 2020 && date.getMonth()+1 == 4 && date.getDate() == 13) {
            return 'holiday';
        }
        // 2021
        if(date.getFullYear() == 2021 && date.getMonth()+1 == 4 && date.getDate() == 5) {
            return 'holiday';
        }
        // 2022
        if(date.getFullYear() == 2022 && date.getMonth()+1 == 4 && date.getDate() == 18) {
            return 'holiday';
        }
        // 2023
        if(date.getFullYear() == 2023 && date.getMonth()+1 == 4 && date.getDate() == 10) {
            return 'holiday';
        }
        // 2024
        if(date.getFullYear() == 2024 && date.getMonth()+1 == 4 && date.getDate() == 1) {
            return 'holiday';
        }
        // end: dates for easter monday
        // begin: dates for corpus christi
        // 2013
        if(date.getFullYear() == 2013 && date.getMonth()+1 == 5 && date.getDate() == 30) {
            return 'holiday';
        }
        // 2014
        if(date.getFullYear() == 2014 && date.getMonth()+1 == 6 && date.getDate() == 19) {
            return 'holiday';
        }
        // 2015
        if(date.getFullYear() == 2015 && date.getMonth()+1 == 6 && date.getDate() == 4) {
            return 'holiday';
        }
        // 2016
        if(date.getFullYear() == 2016 && date.getMonth()+1 == 5 && date.getDate() == 26) {
            return 'holiday';
        }
        // 2017
        if(date.getFullYear() == 2017 && date.getMonth()+1 == 6 && date.getDate() == 15) {
            return 'holiday';
        }
        // 2018
        if(date.getFullYear() == 2018 && date.getMonth()+1 == 5 && date.getDate() == 31) {
            return 'holiday';
        }
        // 2019
        if(date.getFullYear() == 2019 && date.getMonth()+1 == 6 && date.getDate() == 20) {
            return 'holiday';
        }
        // 2020
        if(date.getFullYear() == 2020 && date.getMonth()+1 == 6 && date.getDate() == 11) {
            return 'holiday';
        }
        // 2021
        if(date.getFullYear() == 2021 && date.getMonth()+1 == 6 && date.getDate() == 3) {
            return 'holiday';
        }
        // 2022
        if(date.getFullYear() == 2022 && date.getMonth()+1 == 6 && date.getDate() == 16) {
            return 'holiday';
        }
        // 2023
        if(date.getFullYear() == 2023 && date.getMonth()+1 == 6 && date.getDate() == 8) {
            return 'holiday';
        }
        // 2024
        if(date.getFullYear() == 2024 && date.getMonth()+1 == 5 && date.getDate() == 30) {
            return 'holiday';
        }
        // end: dates for corpus christi
        return '';
    }
});