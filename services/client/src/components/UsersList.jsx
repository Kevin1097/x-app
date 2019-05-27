import React from 'react';

const UsersList = (props) => {
    return(
        <div>
            {
                props.users.map((users) => {
                    return (
                        <h4
                          key={users.id}
                          className="box title is-4"
                        >{ users.username }
                        </h4>
                    )
                })
            }
        </div>
    )
};

export default UsersList;