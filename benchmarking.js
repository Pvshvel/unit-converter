import http from 'k6/http'


export const options = {
    vus: 50,
    duration: '30s'
};

export default function () {
    http.get('http://localhost:8000/convert/weight?from_unit=GRAM&from_value=100&target_unit=KILOGRAM');
}
