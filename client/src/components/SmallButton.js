import React from "react";
import { Grid, Button } from '@material-ui/core';

const SmallButton = (props) => {

    const handleButtonClick = () => {
        // call the parent callback function to send a request to the backend
        props.buttonClicked();
    };

    return (
        <Grid item xs={12} style={{ textAlign:'center' }}>
            <Button 
                variant='contained' 
                color='primary' 
                onClick={handleButtonClick} 
                style={{backgroundColor: '#7b113a'}}
            >
                Add
            </Button>
        </Grid>
    );
};

export default SmallButton;