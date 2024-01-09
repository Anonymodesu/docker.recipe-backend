if [ -n "${INIT_RECIPES_CSV}" ];
then
    echo "Initialising database with ${INIT_RECIPES_CSV}."
    python init_db.py
fi

flask run --host=0.0.0.0