func bmiCategory(weightKg: Double, heightM: Double) -> String {
    let bmi = weightKg / (heightM * heightM)
    let category = if bmi < 18.5 {
        "underweight"
    } else if bmi < 25 {
        "normal"
    } else if bmi < 30 {
        "overweight"
    } else {
        "obese"
    }
    return category
}
