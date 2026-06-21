from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.models.smartphone import Smartphone
from app import db

smartphone_bp = Blueprint('smartphones', __name__)

@smartphone_bp.route('/')
def index():
    search = request.args.get('search', '')
    if search:
        smartphones = Smartphone.query.filter(Smartphone.nama.ilike(f'%{search}%')).all()
    else:
        smartphones = Smartphone.query.all()
    return render_template('smartphones/index.html', smartphones=smartphones, search=search)

@smartphone_bp.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        nama = request.form.get('nama')
        harga = float(request.form.get('harga'))
        foto = float(request.form.get('foto'))
        video = float(request.form.get('video'))
        chipset = float(request.form.get('chipset'))
        baterai = float(request.form.get('baterai'))
        storage = float(request.form.get('storage'))
        new_sp = Smartphone(
            nama=nama, harga=harga, foto=foto, video=video, 
            chipset=chipset, baterai=baterai, storage=storage
        )
        db.session.add(new_sp)
        db.session.commit()
        flash('Data smartphone berhasil ditambahkan!', 'success')
        return redirect(url_for('smartphones.index'))
    return render_template('smartphones/form.html', action="Add", smartphone=None)

@smartphone_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    sp = Smartphone.query.get_or_404(id)
    if request.method == 'POST':
        sp.nama = request.form.get('nama')
        sp.harga = float(request.form.get('harga'))
        sp.foto = float(request.form.get('foto'))
        sp.video = float(request.form.get('video'))
        sp.chipset = float(request.form.get('chipset'))
        sp.baterai = float(request.form.get('baterai'))
        sp.storage = float(request.form.get('storage'))
        
        db.session.commit()
        flash('Data smartphone berhasil diperbarui!', 'success')
        return redirect(url_for('smartphones.index'))
    return render_template('smartphones/form.html', action="Edit", smartphone=sp)

@smartphone_bp.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    sp = Smartphone.query.get_or_404(id)
    db.session.delete(sp)
    db.session.commit()
    flash('Data smartphone berhasil dihapus!', 'success')
    return redirect(url_for('smartphones.index'))
