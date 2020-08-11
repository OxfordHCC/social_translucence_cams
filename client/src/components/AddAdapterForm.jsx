import React from 'react';
import { useParams, useHistory } from 'react-router-dom';
import { connect } from 'react-redux';
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import { postAdapter } from '~/src/actions/adapterActions';

const templateFromClass = (adapterClass) => adapterClass && {
    name: "",
    "adapter_type": adapterClass['type'],
    options: {
        ...(Object.keys(adapterClass.options)
            .reduce((acc, curr) => {
                acc[curr] = "";
                return acc;
            }, {})
           )
    }
};


//TODO: move to separate file
function AddAdapterForm({ adapterClasses, addAdapter }){
    const { adapterType } = useParams();
    const adapterClass = adapterClasses.find(a => a.type === adapterType);
    const [ adapter, setAdapter ] = React.useState(undefined);
    const history = useHistory();

    React.useEffect(() => {
        setAdapter(() => templateFromClass(adapterClass));
    }, [adapterClass]);

    
    //this return is here just to prevent errors while refreshing the
    //page because adapterClass may be null until data is synced
    //(which happens on app load)
    if(!adapter){
        return ''; 
    }
    
    const handleChange = evt => {
        const key = evt.target.name;
        const newAdapter = Object.assign({}, adapter, {
            [key]: evt.target.value
        });
        setAdapter(newAdapter);
    };
    
    const handleOptionsChange = evt => {
        const key = evt.target.name;
        const newAdapter = Object.assign({}, adapter, {
            options:{
                ...adapter.options,
                [key]: evt.target.value
            }
        });
        setAdapter(newAdapter);
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        try{
            addAdapter(adapter);
            history.push('/adapters');
        }catch(err){
            console.error(err);
        }
    };

    const getFields = (schema) => {
        return Object.entries(schema)
            .map(([key, field]) =>
                 <div key={key}>
                   <TextField
                     label={field.name}
                     name={key}
                     onChange={handleOptionsChange}
                     value={adapter.options[key]}
                   />
                 </div>
        );
    };
    
    return (
        <div className="add-adapter-form">
          <h2>Add {adapterClass.name} adapter</h2>
          
          <form onSubmit={handleSubmit}>
            <TextField label="Name"
                       name="name"
                       onChange={handleChange}
                       value={adapter.name}
            />


            <h3> Options</h3>
            <div>
              { getFields(adapterClass.options) }
            </div>
            
            <Button
              type="submit"
              variant="contained"
              color="primary"
              onClick={handleSubmit}
            >
              Submit
            </Button>
          </form>

        </div>
    );
}

const stateToProps = ({ adapterClasses }) => ({
    adapterClasses
});

const dispatchToProps = (dispatch) => ({
    addAdapter: (adapter) => dispatch(postAdapter(adapter))
});

export default connect(stateToProps, dispatchToProps)(AddAdapterForm);
