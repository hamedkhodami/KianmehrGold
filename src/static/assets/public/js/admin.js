document.addEventListener("DOMContentLoaded", function () {
    const categoryField = document.getElementById("id_category");

    const weightField = document.getElementById("id_weight");
    const coinTypeField = document.getElementById("id_coin_type");

    const extraFeeField = document.getElementById("id_market_extra_fee");
    const percentFeeField = document.getElementById("id_market_percent_fee");

    if (!categoryField) {
        return;
    }

    function getRow(field) {
        return field ? field.closest(".form-row") : null;
    }

    function show(row) {
        if (row) {
            row.style.display = "";
        }
    }

    function hide(row) {
        if (row) {
            row.style.display = "none";
        }
    }

    function updateFields() {
        const category = categoryField.value;

        const weightRow = getRow(weightField);
        const coinTypeRow = getRow(coinTypeField);
        const extraFeeRow = getRow(extraFeeField);
        const percentFeeRow = getRow(percentFeeField);

        // =========================================
        // BANK
        // فقط Coin Type
        // =========================================
        if (category === "bank") {
            hide(weightRow);
            show(coinTypeRow);
            hide(extraFeeRow);
            hide(percentFeeRow);

            if (extraFeeField) {
                extraFeeField.value = "";
            }

            if (percentFeeField) {
                percentFeeField.value = "";
            }
        }

        // =========================================
        // MARKET
        // Coin Type + Fee
        // =========================================
        else if (category === "market") {
            hide(weightRow);
            show(coinTypeRow);
            show(extraFeeRow);
            show(percentFeeRow);

            if (extraFeeField) {
                extraFeeField.readOnly = false;
            }

            if (percentFeeField) {
                percentFeeField.readOnly = false;
            }
        }

        // =========================================
        // PARSIAN
        // Weight + Fee
        // =========================================
        else if (category === "parsian") {
            show(weightRow);
            hide(coinTypeRow);
            show(extraFeeRow);
            show(percentFeeRow);

            if (extraFeeField) {
                extraFeeField.readOnly = false;
            }

            if (percentFeeField) {
                percentFeeField.readOnly = false;
            }
        }

        // =========================================
        // EMPTY
        // =========================================
        else {
            hide(weightRow);
            show(coinTypeRow);
            hide(extraFeeRow);
            hide(percentFeeRow);
        }
    }

    // اجرای اولیه
    updateFields();

    // هنگام تغییر Category
    categoryField.addEventListener("change", updateFields);
});