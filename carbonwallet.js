document.addEventListener('DOMContentLoaded', () => {
    // Carbon Calculator Logic
    const calculateButton = document.getElementById('calculate-carbon');
    const transportType = document.getElementById('transport-type');
    const transportDistance = document.getElementById('transport-distance');
    const electricityUsage = document.getElementById('electricity-usage');
    const dietType = document.getElementById('diet-type');

    const carbonResult = document.getElementById('carbon-result');
    const transportCarbon = document.getElementById('transport-carbon');
    const energyCarbon = document.getElementById('energy-carbon');
    const dietCarbon = document.getElementById('diet-carbon');
    const carbonTips = document.getElementById('carbon-tips');

    const carbonSavedElement = document.getElementById('carbon-saved');
    const treesEquivalentElement = document.getElementById('trees-equivalent');

    const carbonTipDatabase = {
        transport: {
            car: "Consider carpooling or using public transit to reduce emissions.",
            publicTransit: "Great choice! Public transit significantly reduces per-person carbon emissions.",
            bicycle: "Cycling is an excellent zero-emission transportation method!",
            walking: "Walking produces zero carbon emissions - keep it up!"
        },
        energy: {
            low: "Try using energy-efficient appliances and LED lighting.",
            medium: "Consider solar panels or switching to a green energy provider.",
            high: "Look into home insulation and smart energy management systems."
        },
        diet: {
            "meat-heavy": "Reducing meat consumption can significantly lower your carbon footprint.",
            "balanced": "You're on the right track! Try increasing plant-based meals.",
            "vegetarian": "Plant-based diets have a lower environmental impact.",
            "vegan": "Your diet has an extremely low carbon footprint!"
        }
    };

    calculateButton.addEventListener('click', () => {
        const transportEmissionFactors = {
            'Car': 0.192,  // kg CO2 per km
            'Public Transit': 0.089,
            'Bicycle': 0,
            'Walking': 0
        };

        const energyEmissionFactors = {
            low: 0.1,    // kg CO2 per kWh
            medium: 0.3,
            high: 0.5
        };

        const dietEmissionFactors = {
            'Meat-heavy': 3.3,   // kg CO2 per day
            'Balanced': 2.5,
            'Vegetarian': 1.7,
            'Vegan': 1.0
        };

        const transportEmissions = transportDistance.value * transportEmissionFactors[transportType.value];
        const energyEmissions = electricityUsage.value * energyEmissionFactors[
            electricityUsage.value < 100 ? 'low' : 
            electricityUsage.value < 300 ? 'medium' : 'high'
        ];
        const dietEmissions = dietEmissionFactors[dietType.value];

        const totalEmissions = transportEmissions + energyEmissions + dietEmissions;

        // Update results
        carbonResult.textContent = totalEmissions.toFixed(2);
        transportCarbon.textContent = transportEmissions.toFixed(2);
        energyCarbon.textContent = energyEmissions.toFixed(2);
        dietCarbon.textContent = dietEmissions.toFixed(2);

        // Generate tips
        carbonTips.innerHTML = '';
        [
            carbonTipDatabase.transport[transportType.value.toLowerCase()],
            carbonTipDatabase.energy[
                electricityUsage.value < 100 ? 'low' : 
                electricityUsage.value < 300 ? 'medium' : 'high'
            ],
            carbonTipDatabase.diet[dietType.value.toLowerCase()]
        ].forEach(tip => {
            const li = document.createElement('li');
            li.textContent = tip;
            carbonTips.appendChild(li);
        });
    });

    // Newsletter Signup
    const newsletterForm = document.getElementById('newsletter-form');
    newsletterForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const email = newsletterForm.querySelector('input').value;
        alert(`Thank you for subscribing with ${email}! We'll keep you updated.`);
        newsletterForm.reset();
    });

    // Animated Number Counters
    function animateValue(element, start, end, duration) {
        let startTimestamp = null;
        const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            element.textContent = Math.floor(progress * (end - start) + start);
            if (progress < 1) {
                window.requestAnimationFrame(step);
            }
        };
        window.requestAnimationFrame(step);
    }

    // Carbon Saved & Trees Equivalent Animation
    if (carbonSavedElement && treesEquivalentElement) {
        animateValue(carbonSavedElement, 0, 500, 2000);
        animateValue(treesEquivalentElement, 0, 25, 2000);
    }
});