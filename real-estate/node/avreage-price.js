const fs = require("fs");

var input_folder = "/data/inputs";
var output_folder = "/data/outputs";

async function processfolder(Path) {
    var files = fs.readdirSync(Path);
    console.log(`files: ${files}`)
    for (var i = 0; i < files.length; i++) {
        var file = files[i];
        var fullpath = Path + "/" + file;
        if (fs.statSync(fullpath).isDirectory()) {
            await processfolder(fullpath);
        } else {
            console.log(`path to file: ${fullpath}`)
            computeAvgPrice(fullpath);
        }
    }
}
processfolder(input_folder);

function computeAvgPrice(filepath) {
    const properties = JSON.parse(
        fs.readFileSync(filepath, "utf8")
    );

    console.log(`Properties: ${properties}`);

    const avgPricesByRooms = {};

    properties.forEach((property) => {
        const { info } = property;
        const { price, roomsNo } = info;

        if (!avgPricesByRooms[roomsNo]) {
            avgPricesByRooms[roomsNo] = {
                totalPrice: 0,
                count: 0,
            };
        }

        avgPricesByRooms[roomsNo].totalPrice += price;
        avgPricesByRooms[roomsNo].count++;
    });

    for (const roomsNo in avgPricesByRooms) {
        avgPricesByRooms[roomsNo].averagePrice =
            avgPricesByRooms[roomsNo].totalPrice / avgPricesByRooms[roomsNo].count;
        avgPricesByRooms[roomsNo].averagePrice = parseFloat(
            avgPricesByRooms[roomsNo].averagePrice.toFixed(2)
        );
    }

    const outputFile = `${output_folder}/results.json`;

    fs.writeFileSync(outputFile, JSON.stringify(avgPricesByRooms, null, 2));

    console.log(`Avg prices: ${avgPricesByRooms}`);
}
