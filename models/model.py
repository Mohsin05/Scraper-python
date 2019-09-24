from __future__ import unicode_literals, print_function
import spacy
import random
import plac
import random
from pathlib import Path
import spacy
from spacy.util import minibatch, compounding

TRAIN_DATA = [
                ('Watsi Is Hiring an Executive Director of Crowdfunding', {'entities': [(0, 4, 'company_name'),(19,37,'job_title')]}),
                ('ReadMe (YC W15) is hiring. Help us make APIs easy to use', {'entities': [(0, 5, 'company_name'),(40,55,'job_title')]}),
                ('Scale AI is hiring engineers to accelerate the development of AI', {'entities': [(0, 7, 'company_name'),(47,63,'job_title')]}),
                ('Jerry (YC S17) Is Hiring Senior Software Developers (Toronto Canada; Remote)', {'entities': [(0, 4, 'company_name'),(25,50,'job_title'), (53,66,'location')]}),
                 ('Smarking (YC W15) hiring a senior back-end engineer to scale data infrastructure', {'entities': [(0, 7, 'company_name'),(27,50,'job_title')]}),
                 ('Taplytics (YC W14) Is Hiring an Engineering Lead in Toronto to Help Us Scale', {'entities': [(0, 8, 'company_name'),(32,42,'job_title'), (52,58,'location')]}),
                  ('Quartzy (YC S11) is hiring a Sr SRE – remote and first of platform team', {'entities': [(0, 6, 'company_name'),(29,34,'job_title')]}),
                  ('Cloosiv (YC S19) Is Hiring a Full-Stack Engineer', {'entities': [ (0, 6, 'company_name'),(40,47,'job_title') ]}),


                  ('Bitmovin (YC S15) Hires a Support Engineer in Denver', {'entities': [(0, 7, 'company_name'),(26,33,'job_title'), (46,51,'location')]}),
                  ('Mino Games (YC W11) Is Hiring Game Developers in Montreal, QC', {'entities': [(0, 9, 'company_name'),(5,19,'job_title'), (46,56,'location')]}),


                  ('Mux is hiring a PM to build monitoring for the largest streaming events ever', {'entities': [(0, 7, 'company_name'),(16,17,'job_title')]}),
                  ('Atomwise (YC W15) Is Hiring a Senior Software Engineer', {'entities': [(0, 7, 'company_name'),(30,53,'job_title')]}),
                  ('BuildZoom (YC W13) is hiring – help us build better homes', {'entities': [(0, 8, 'company_name'),(42,53,'job_title')]}),
                  ('New Story (YC Nonprofit) Hiring Customer Success Specialist', {'entities': [(0, 8, 'company_name'),(49,58,'job_title')]}),




                   ]

@plac.annotations(
    model=("Model name. Defaults to blank 'en' model.", "option", "m", str),
    output_dir='("Optional output directory", "option", "o", Path)',
    n_iter=("Number of training iterations", "option", "n", int),
)
def main(model=None, output_dir='./en_ycombinator_model', n_iter=100):
    """Load the model, set up the pipeline and train the entity recognizer."""
    if model is not None:
        nlp = spacy.load(model)  # load existing spaCy model
        print("Loaded model '%s'" % model)
    else:
        nlp = spacy.blank("en")  # create blank Language class
        print("Created blank 'en' model")

    # create the built-in pipeline components and add them to the pipeline
    # nlp.create_pipe works for built-ins that are registered with spaCy
    if "ner" not in nlp.pipe_names:
        ner = nlp.create_pipe("ner")
        nlp.add_pipe(ner, last=True)
    # otherwise, get it so we can add labels
    else:
        ner = nlp.get_pipe("ner")

    # add labels
    for _, annotations in TRAIN_DATA:
        for ent in annotations.get("entities"):
            ner.add_label(ent[2])

    # get names of other pipes to disable them during training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
    with nlp.disable_pipes(*other_pipes):  # only train NER
        # reset and initialize the weights randomly – but only if we're
        # training a new model
        if model is None:
            nlp.begin_training()
        for itn in range(n_iter):
            random.shuffle(TRAIN_DATA)
            losses = {}
            # batch up the examples using spaCy's minibatch
            batches = minibatch(TRAIN_DATA, size=compounding(4.0, 32.0, 1.001))
            for batch in batches:
                texts, annotations = zip(*batch)
                nlp.update(
                    texts,  # batch of texts
                    annotations,  # batch of annotations
                    drop=0.5,  # dropout - make it harder to memorise data
                    losses=losses,
                )
            print("Losses", losses)

    # test the trained model
    for text, _ in TRAIN_DATA:
        doc = nlp(text)
        print("Entities", [(ent.text, ent.label_) for ent in doc.ents])
        print("Tokens", [(t.text, t.ent_type_, t.ent_iob) for t in doc])

    # save model to output directory
    if output_dir is not None:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()
        nlp.to_disk(output_dir)
        print("Saved model to", output_dir)

        # test the saved model
        print("Loading from", output_dir)
        nlp2 = spacy.load(output_dir)
        for text, _ in TRAIN_DATA:
            doc = nlp2(text)
            print("Entities", [(ent.text, ent.label_) for ent in doc.ents])
            print("Tokens", [(t.text, t.ent_type_, t.ent_iob) for t in doc])


if __name__ == "__main__":
    plac.call(main)
