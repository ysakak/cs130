
/**
 * Provides suggestions for state names (USA).
 * @class
 * @scope public
 */
function StateSuggestions() {
    this.states = [
"Aerospace Studies ", "African American Studies ", "Afrikaans ", "American Indian Studies ", "American Sign Language ",
"Ancient Near East ", "Anthropology ", "Applied Linguistics ", "Arabic ", "Archaeology ", "Architecture and Urban Design ",
"Armenian ", "Art ", "Art History ", "Arts Education ", "Arts and Architecture ", "Asian ", "Asian American Studies ",
"Astronomy ", "Atmospheric and Oceanic Sciences  ", "Bioengineering ", "Bioinformatics (Graduate) ", "Biological Chemistry ",
"Biomathematics ", "Biomedical Research ", "Biostatistics ", "Central and East European Studies ", "Chemical Engineering ",
"Chemistry and Biochemistry ", "Chicana and Chicano Studies ", "Chinese ", "Civic Engagement ", "Civil and Environmental Engineering ",
"Classics ", "Communication Studies ", "Community Health Sciences ", "Comparative Literature ", "Computational and Systems Biology ",
"Computer Science ", "Conservation of Archaeological Ethnographic Materials ", "Dance ", "Design | Media Arts ", "Digital Humanities ",
"Disability Studies ", "Dutch ", "Earth, Planetary, and Space Sciences ", "Ecology and Evolutionary Biology  ", "Economics ",
"Education ", "Electrical Engineering ", "Engineering ", "English ", "English Composition ", "Environment ",
"Environmental Health Sciences ", "Epidemiology ", "Ethnomusicology ", "Filipino ", "Film and Television ", "French ", "Gender Studies ",
"General Education Clusters ", "Geography ", "German ", "Gerontology ", "Global Studies ", "Greek ", "Health Policy and Management ",
"Hebrew ", "Hindi-Urdu ", "History ", "Honors Collegium ", "Human Genetics ", "Hungarian ", "Indigenous Languages of the Americas  ",
"Indo-European Studies ", "Indonesian ", "Information Studies ", "International Development Studies ", "International and Area Studies ",
"Iranian ", "Islamic Studies ", "Italian ", "Japanese ", "Jewish Studies ", "Korean ", "Labor and Workplace Studies ",
"Latin ", "Latin American Studies ", "Law, Undergraduate ", "Life Sciences ", "Linguistics ", "Management ", "Materials Science and Engineering ",
"Mathematics ", "Mechanical and Aerospace Engineering ", "Medical History ", "Microbiology, Immunology, and Molecular Genetics ",
"Middle Eastern Studies ", "Military Science ", "Molecular Biology ", "Molecular Toxicology ", "Molecular and Medical Pharmacology ",
"Molecular, Cell, and Developmental Biology ", "Molecular, Cellular, and Integrative Physiology ", "Music ", "Music History ", "Music Industry ",
"Musicology ", "Naval Science ", "Near Eastern Languages ", "Neurobiology ", "Neurology ", "Neuroscience ", "Neuroscience (Graduate) ", "Nursing ",
"Oral Biology ", "Pathology and Laboratory Medicine ", "Philosophy ", "Physics ", "Physics and Biology in Medicine ", "Physiological Science ",
"Polish ", "Political Science ", "Portuguese ", "Program in Computing ", "Psychiatry and Biobehavioral Sciences ", "Psychology ", "Public Health ",
"Public Policy ", "Religion, Study of ", "Romanian ", "Russian ", "Scandinavian ", "Science Education ", "Semitic ", "Serbian/Croatian ",
"Slavic ", "Social Thought ", "Social Welfare ", "Society and Genetics ", "Sociology ", "South Asian ", "Southeast Asian ", "Spanish ",
"Statistics ", "Surgery ", "Swahili ", "Thai ", "Theater ", "Turkic Languages ", "University Studies ", "Urban Planning ", "Vietnamese ",
"World Arts and Cultures ", "Yiddish ",
 
    ];
}

/**
 * Request suggestions for the given autosuggest control. 
 * @scope protected
 * @param oAutoSuggestControl The autosuggest control to provide suggestions for.
 */
StateSuggestions.prototype.requestSuggestions = function (oAutoSuggestControl /*:AutoSuggestControl*/,
                                                          bTypeAhead /*:boolean*/) {
    var aSuggestions = [];
    var sTextboxValue = oAutoSuggestControl.textbox.value;
    
    if (sTextboxValue.length > 0){
    
        //search for matching states
        for (var i=0; i < this.states.length; i++) { 
            if (this.states[i].indexOf(sTextboxValue) == 0 ||
                this.states[i].toLowerCase().indexOf(sTextboxValue) == 0) {
                aSuggestions.push(this.states[i]);
            } 
        }
    }

    //provide suggestions to the control
    oAutoSuggestControl.autosuggest(aSuggestions, bTypeAhead);
};