import React from 'react';

const FiltersComponent = props =>{
  const cities={
    margin: "20px",
    position: "center",
  }

  let CityOptions=props.cities.map(city => {
    return (
      <option key={city.id} value={city.id}>{city.name}</option>
    )
  });

  return (
    <div className="form-inline">
      <div className="form-group">
        <label htmlFor="cities">Search by City</label>
        <select id="cities" style={cities} className="form-control" onChange={props.handleCitySearch}>
            <option key="0" value="0">Choose City</option>
            {CityOptions}
        </select>
      </div>
    </div>
  );

}

export default FiltersComponent;
