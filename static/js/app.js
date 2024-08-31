async function deleteAllSignals() {
    try {
        const response = await fetch('/signals', {
            method: "DELETE",
            headers: {
                'Content-Type': 'application/json'
            },
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail.msg);
        }

        const responseData = await response.json();
        alert(responseData.msg);
    } catch (error) {
        alert(error.message);
    }
}


async function sendSignal() {
    const type = document.getElementById('type_').value;
    const priceElement = document.getElementById('price');

    const data = {
        type_: type,
        tp: parseFloat(document.getElementById('tp').value),
        sl: parseFloat(document.getElementById('sl').value),
    };

    if (type === 'PENDING_BUY' || type === 'PENDING_SELL') {
        data.price = parseFloat(priceElement.value);
    } else {
        delete data.price;
    }

    try {
        const response = await fetch('/signals', {
            method: "POST",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail[0]?.msg || 'Unknown error');
        }

        const responseData = await response.json();
        alert(responseData.msg);
    } catch (error) {
        alert(error.message);
    }
}


async function closeAllSignals() {
    const SignalType = {
        BUY: "BUY",
        SELL: "SELL",
        PENDING_BUY: "PENDING_BUY",
        PENDING_SELL: "PENDING_SELL",
        CLOSED: "CLOSED"
    };
    const type = SignalType.CLOSED; // Используйте значение из объекта SignalType
    const data = {
        type_: type,
    };
    try {
        const response = await fetch('/signals', {
            method: "PATCH",
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail.msg);
        }

        const responseData = await response.json();
        alert(responseData.msg);
    } catch (error) {
        alert(error.message);
    }
}
